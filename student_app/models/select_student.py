import tkinter as tk
from tkinter import messagebox
import sqlite3

# Lấy thông tin sinh viên được chọn từ bảng
def get_selected_student(student_table):
    selected_item = student_table.selection()
    if not selected_item:
        return None
    return student_table.item(selected_item, "values")

# Hàm xử lý khi chọn sinh viên (single click / chọn dòng)
def on_student_select(app, event=None):
    selected_student = get_selected_student(app.ui.student_table)

    if selected_student:
        app.ui.semester_entry.delete(0, tk.END)
        app.ui.semester_entry.insert(0, selected_student[0])

        app.ui.class_code_entry.delete(0, tk.END)
        app.ui.class_code_entry.insert(0, selected_student[1])

        app.ui.subject_name_entry.delete(0, tk.END)
        app.ui.subject_name_entry.insert(0, selected_student[2])

        app.ui.student_name_entry.delete(0, tk.END)
        app.ui.student_name_entry.insert(0, selected_student[3])

        app.ui.mssv_entry.delete(0, tk.END)
        app.ui.mssv_entry.insert(0, selected_student[4])

# Hàm xử lý double click để hiện popup thông tin nghỉ học
def on_student_double_click(app, event=None):
    selected_student = get_selected_student(app.ui.student_table)

    if selected_student:
        student_name = selected_student[3]
        mssv = selected_student[4]
        show_student_info_popup(student_name, mssv)

# Hàm hiển thị thông tin ngày nghỉ của sinh viên
def show_student_info_popup(student_name, mssv):
    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT thoi_gian_nghi FROM students WHERE mssv = ?", (mssv,))
        result = c.fetchone()
        conn.close()

        if result:
            thoi_gian_nghi = result[0]
            if not thoi_gian_nghi:
                messagebox.showinfo("Thông tin sinh viên", f"Tên: {student_name}\nSinh viên không nghỉ ngày nào!")
            else:
                days_off = thoi_gian_nghi.split(";")
                days_off_message = "\n".join(days_off)
                messagebox.showinfo("Thông tin sinh viên", f"Tên: {student_name}\nNgày nghỉ:\n{days_off_message}")
        else:
            messagebox.showinfo("Thông tin sinh viên", "Không tìm thấy thông tin ngày nghỉ.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
