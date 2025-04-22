import tkinter as tk

def refresh_table(app):
    app.load_students()
    app.ui.search_entry.delete(0, tk.END)  # Xóa ô tìm kiếm nếu có
    app.ui.semester_entry.delete(0, tk.END)
    app.ui.class_code_entry.delete(0, tk.END)
    app.ui.subject_name_entry.delete(0, tk.END)
    app.ui.student_name_entry.delete(0, tk.END)
    app.ui.mssv_entry.delete(0, tk.END)