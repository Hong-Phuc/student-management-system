import sqlite3
from tkinter import messagebox

from student_app.models.undo_redo import save_state

def save_info(app):
    """Lưu hoặc cập nhật thông tin sinh viên."""
    # Lấy thông tin từ các ô nhập
    semester = app.ui.semester_entry.get()
    class_code = app.ui.class_code_entry.get()
    subject_name = app.ui.subject_name_entry.get()
    student_name = app.ui.student_name_entry.get()
    mssv = app.ui.mssv_entry.get()

    # Lấy sinh viên được chọn từ bảng
    selected_student = app.get_selected_student()

    # Kiểm tra xem đã nhập đủ thông tin chưa
    if semester and class_code and subject_name and student_name and mssv:
        try:
            # Lưu trạng thái hiện tại trước khi thay đổi
            save_state()

            # Kết nối đến cơ sở dữ liệu SQLite
            conn = sqlite3.connect('data.db')
            c = conn.cursor()

            if selected_student:
                # Cập nhật thông tin sinh viên nếu đã chọn sinh viên
                c.execute("UPDATE students SET semester=?, class_code=?, subject_name=?, student_name=? WHERE mssv=?",
                          (semester, class_code, subject_name, student_name, selected_student[4]))
                messagebox.showinfo("Update Info", "Thông tin sinh viên đã được cập nhật thành công!")
            else:
                # Thêm sinh viên mới nếu chưa có sinh viên được chọn
                c.execute("INSERT INTO students (semester, class_code, subject_name, student_name, mssv) VALUES (?, ?, ?, ?, ?)",
                          (semester, class_code, subject_name, student_name, mssv))
                messagebox.showinfo("Save Info", "Thông tin sinh viên đã được lưu thành công!")

            # Lưu thay đổi vào cơ sở dữ liệu
            conn.commit()
            conn.close()

            # Cập nhật lại danh sách sinh viên và làm mới giao diện
            app.load_students()
            app.refresh_table()

        except sqlite3.Error as e:
            # Xử lý lỗi nếu có vấn đề khi thao tác với cơ sở dữ liệu
            messagebox.showerror("Database Error", f"Đã xảy ra lỗi khi lưu thông tin: {e}")

    else:
        # Thông báo nếu người dùng chưa nhập đầy đủ thông tin
        messagebox.showerror("Save Info", "Vui lòng điền đầy đủ thông tin sinh viên.")
