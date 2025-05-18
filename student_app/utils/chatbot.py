import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
import re
from unidecode import unidecode

# Tải biến môi trường từ file .env
load_dotenv(os.path.join("config", ".env"))

def generate_sql_query(question):
    try:
        api_key = os.getenv("HUGGING_FACE_API_KEY")
        client = OpenAI(
            api_key=api_key,
            base_url="https://router.huggingface.co/fireworks-ai/inference/v1"
        )

        # Nếu là câu hỏi về lớp của sinh viên
        match_class = re.search(r"sinh viên (.+?) học lớp nào", question.lower())
        if match_class:
            student_name = match_class.group(1).strip().title()
            with sqlite3.connect('data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT class_code FROM students WHERE student_name = ?", (student_name,))
                result = cursor.fetchone()
                if result:
                    class_code = result[0]
                    return f"Sinh viên {student_name} học lớp {class_code}."
                else:
                    return f"Không tìm thấy sinh viên {student_name}."

        # Nếu là câu hỏi về số ngày nghỉ của sinh viên
        match = re.search(r"sinh viên (.+?) nghỉ mấy ngày", question.lower())
        if match:
            student_name = match.group(1).strip().title()
            with sqlite3.connect('data.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT so_ngay_nghi, thoi_gian_nghi FROM students WHERE student_name = ?", (student_name,))
                result = cursor.fetchone()
                if result:
                    so_ngay_nghi, thoi_gian_nghi = result
                    if so_ngay_nghi > 0:
                        # Xử lý danh sách ngày nghỉ và số tiết, mỗi ngày 1 dòng
                        ngay_nghi_list = [ngay.strip() for ngay in thoi_gian_nghi.split(";") if ngay.strip()]
                        ngay_nghi_str = "\n".join(ngay_nghi_list)
                        return f"Sinh viên {student_name} nghỉ {so_ngay_nghi} ngày:\n{ngay_nghi_str}"
                    else:
                        return f"Sinh viên {student_name} không nghỉ buổi nào."
                else:
                    return f"Không tìm thấy sinh viên {student_name}."

        # Prompt AI cho các câu hỏi khác
        prompt = f"""
Bạn là một chatbot hỗ trợ quản lý sinh viên. 
Chỉ trả lời ngắn gọn, tự nhiên, không trả về JSON, không giải thích, không lặp lại câu hỏi.
Ví dụ:
Hỏi: Có mấy sinh viên tên Anh?
Trả lời: Có 3 sinh viên tên Anh trong hệ thống.
---
Câu hỏi: {question}
Trả lời:
"""
        completion = client.chat.completions.create(
            model="accounts/fireworks/models/deepseek-v3-0324",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        message = completion.choices[0].message
        response_text = message.content.strip()
        response_text = response_text.replace("```sql", "").replace("```", "").strip()

        # Nếu là câu hỏi về số lượng sinh viên, thực hiện truy vấn SQL
        if "có mấy sinh viên" in question.lower() or "có bao nhiêu sinh viên" in question.lower():
            try:
                # Trích xuất tên từ câu hỏi, loại bỏ dấu câu và chuẩn hóa tên
                name_raw = question.lower().split("tên")[-1]
                name = re.sub(r'[^a-zA-ZÀ-ỹ\s]', '', name_raw).strip()
                name = ' '.join([w.capitalize() for w in name.split()])
                name_ascii = unidecode(name).lower()
                if name:
                    with sqlite3.connect('data.db') as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT student_name FROM students")
                        all_names = cursor.fetchall()
                        count = 0
                        for (full_name,) in all_names:
                            last_name = full_name.strip().split()[-1]
                            last_name_ascii = unidecode(last_name).lower()
                            if last_name_ascii == name_ascii:
                                count += 1
                        response_text = f"Có {count} sinh viên tên {name} trong hệ thống"
            except Exception as e:
                print(f"Lỗi khi đếm số lượng sinh viên: {e}")

        return response_text
    except Exception as e:
        print(f"Lỗi API từ Inference Providers: {e}")
        return "Lỗi kết nối API."

def execute_sql_query(sql_query):
    try:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Nếu không có kết quả
            if not rows:
                return [("Không có kết quả.",)]

            # Định dạng kết quả để trả lời tự nhiên
            result = []
            for row in rows:
                student_name = row[0]
                so_ngay_nghi = row[1]
                thoi_gian_nghi = row[2]

                if so_ngay_nghi > 0:
                    ngay_nghi_list = thoi_gian_nghi.split("; ")
                    ngay_nghi_str = ", ".join(ngay_nghi_list)
                    result.append((f"Sinh viên {student_name} nghỉ {so_ngay_nghi} ngày: {ngay_nghi_str}",))
                else:
                    result.append((f"Sinh viên {student_name} không nghỉ buổi nào.",))

            return result
    except Exception as e:
        print(f"Lỗi truy vấn SQL: {e}")
        return [("Lỗi truy vấn SQL.",)]
