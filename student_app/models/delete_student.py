import sqlite3
from tkinter import messagebox
from student_app.models.undo_redo import save_state


def delete_student(app):
    selected_student = app.get_selected_student()  # Lấy sinh viên được chọn từ bảng
    if selected_student:
        semester, class_code, subject_name, student_name, mssv, so_ngay_nghi = selected_student
        
        # Thêm hộp thoại xác nhận
        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa sinh viên:\n\n"
            f"Họ tên: {student_name}\n"
            f"MSSV: {mssv}\n"
            f"Lớp: {class_code}\n"
            f"Môn học: {subject_name}"
        )
        
        # Chỉ xóa khi người dùng xác nhận Yes
        if confirm:
            save_state()
            try:
                conn = sqlite3.connect('data.db')
                c = conn.cursor()
                c.execute("DELETE FROM students WHERE semester = ? AND class_code = ? AND subject_name = ? AND student_name = ? AND mssv = ? AND so_ngay_nghi = ?",
                          (semester, class_code, subject_name, student_name, mssv, so_ngay_nghi))
                conn.commit()
                conn.close()

                # Hiển thị thông báo thành công
                messagebox.showinfo("Xóa thành công", "Sinh viên đã được xóa khỏi hệ thống!")
                
                # Cập nhật lại bảng sau khi xóa
                app.refresh_table()
                app.load_students()  # Load lại danh sách sinh viên từ DB
                
            except sqlite3.Error as e:
                # Xử lý lỗi khi xóa sinh viên
                messagebox.showerror("Lỗi", f"Không thể xóa sinh viên. Lỗi: {e}")
    else:
        messagebox.showwarning("Xóa không thành công", "Không có sinh viên nào được chọn.")
