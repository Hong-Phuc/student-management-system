import sqlite3
from tkinter import messagebox, simpledialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import openpyxl
import os

# Hàm gửi email
def on_send_email():
    # Tạo danh sách sinh viên nghỉ quá 20% và 50%
    students_over_20 = []
    students_over_50 = []

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi, semester, class_code FROM students")
    students = c.fetchall()
    conn.close()

    for student in students:
        student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi, semester, class_code = student

        # Chuyển đổi phan_tram_vang thành số thực
        if isinstance(phan_tram_vang, str):
            try:
                phan_tram_vang = float(phan_tram_vang.replace(',', '.'))
            except ValueError:
                phan_tram_vang = 0.0
        elif isinstance(phan_tram_vang, (int, float)):
            phan_tram_vang = float(phan_tram_vang)
        else:
            phan_tram_vang = 0.0

        # Thêm thông tin thời gian nghỉ
        if phan_tram_vang >= 50:
            students_over_50.append((student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi, semester, class_code))
        elif phan_tram_vang >= 20:
            students_over_20.append((student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi, semester, class_code))

    # Tạo file Excel cho sinh viên nghỉ quá 20%
    workbook_20 = openpyxl.Workbook()
    sheet_20 = workbook_20.active
    sheet_20.title = "Sinh Viên Vắng > 20%"

    # Tiêu đề cột
    sheet_20.append(["Lớp", "Môn Học", "MSSV", "Họ và Tên", "Tổng Số Ngày Vắng", "% Vắng", "Thời Gian Nghỉ"])

    # Thêm sinh viên nghỉ quá 20%
    for student in students_over_20:
        student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi, semester, class_code = student
        sheet_20.append([class_code, semester, mssv, student_name, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi])

    # Lưu file Excel cho sinh viên nghỉ quá 20%
    file_name_20 = "Danh_sach_sinh_vien_vang_qua_20%.xlsx"
    workbook_20.save(file_name_20)

    # Tạo file Excel cho sinh viên nghỉ quá 50%
    workbook_50 = openpyxl.Workbook()
    sheet_50 = workbook_50.active
    sheet_50.title = "Sinh Viên Vắng > 50%"

    # Tiêu đề cột
    sheet_50.append(["Lớp", "Môn Học", "MSSV", "Họ và Tên", "Tổng Số Ngày Vắng", "% Vắng", "Thời Gian Nghỉ"])

    # Thêm sinh viên nghỉ quá 50%
    for student in students_over_50:
        student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi, semester, class_code = student
        sheet_50.append([class_code, semester, mssv, student_name, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi])

    # Lưu file Excel cho sinh viên nghỉ quá 50%
    file_name_50 = "Danh_sach_sinh_vien_vang_qua_50%.xlsx"
    workbook_50.save(file_name_50)

    # Hiển thị cửa sổ xác nhận
    confirm_message = (
        f"Có {len(students_over_20)} sinh viên nghỉ quá 20% và "
        f"{len(students_over_50)} sinh viên nghỉ quá 50%. Bạn có muốn gửi email danh sách các sinh viên đó không?"
    )

    if messagebox.askyesno("Xác nhận gửi email", confirm_message):
        # Hiển thị ô nhập địa chỉ email người nhận
        receiver_email = simpledialog.askstring("Nhập Email", "Nhập địa chỉ email người nhận:")
        
        if not receiver_email:
            messagebox.showwarning("Cảnh báo", "Bạn cần nhập địa chỉ email người nhận!")
            return  # Dừng nếu không có địa chỉ email

        # Chuẩn bị nội dung email
        sender_email = "hongphuc7167@gmail.com"
        subject = "Danh sách sinh viên nghỉ quá 20% và 50% số tiết"
        
        body = "<h3>Danh sách sinh viên nghỉ quá 20% và 50% số tiết đã được đính kèm.</h3>"

        # Tạo email
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        message.attach(MIMEText(body, "html"))  

        # Đính kèm file Excel
        for file_name in [file_name_20, file_name_50]:
            with open(file_name, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="xlsx")
                attach.add_header('Content-Disposition', 'attachment', filename=file_name)
                message.attach(attach)

        # Gửi email
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender_email, "nxnq jygt fqwz pcmv")  # Nhập mật khẩu của bạn
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()
            messagebox.showinfo("Gửi email", "Email đã được gửi thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi gửi email", f"Không thể gửi email: {str(e)}")
        
        # Xóa file Excel sau khi gửi
        os.remove(file_name_20)  # Xóa file Excel đã tạo sau khi gửi
        os.remove(file_name_50)
    else:
        messagebox.showinfo("Gửi email", "Hành động đã bị hủy.")
