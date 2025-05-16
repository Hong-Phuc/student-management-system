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
        # Lấy API key từ môi trường
        api_key = os.getenv("HUGGING_FACE_API_KEY")

        # Khởi tạo client với API từ Fireworks Inference
        client = OpenAI(
            api_key=api_key,
            base_url="https://router.huggingface.co/fireworks-ai/inference/v1"
        )

        # Prompt tối ưu hóa để trả về câu trả lời hoàn chỉnh
        prompt = f"""
        Bạn là một chuyên gia SQL và trả lời câu hỏi. 
        Hãy trả lời câu hỏi theo cấu trúc, không in ra câu lệnh SQL, không giải thích gì thêm.
        Câu hỏi: {question}.
        Cấu trúc câu trả lời:
        - Nếu người dùng chào: "Chào bạn, tôi là chatbot hỗ trợ bạn trong các 
        - Nếu có nghỉ: "Sinh viên [tên] nghỉ [số ngày] ngày: [danh sách ngày nghỉ]".
        - Nếu không nghỉ: "Sinh viên [tên] không nghỉ buổi nào".
        - Nếu là câu hỏi về ngày nghỉ: "Sinh viên [tên] nghỉ [số ngày] ngày: [danh sách ngày nghỉ]"
        - Nếu là câu hỏi đếm sinh viên: "Có [số lượng] sinh viên có tên [tên] trong hệ thống".
        - Nếu câu hỏi là tìm kiếm sinh viên: "Các sinh viên có tên [tên] được tìm thấy: [danh sách sinh viên]".
        - Nếu cơ sở dữ liệu không có sinh viên nào: "Cơ sở dữ liệu hiện đang trống, hãy thêm danh sách sinh viên".
        - Nếu không có dữ liệu: "Không có sinh viên nào thỏa mãn điều kiện".
        """
        # Gọi mô hình với câu hỏi
        completion = client.chat.completions.create(
            model="accounts/fireworks/models/deepseek-v3-0324",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Lấy câu trả lời từ kết quả trả về
        message = completion.choices[0].message
        response_text = message.content.strip()

        # Loại bỏ ký hiệu không mong muốn
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
