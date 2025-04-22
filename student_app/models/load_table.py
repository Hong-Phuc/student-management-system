import sqlite3

def load_students(student_table):
    # Xóa tất cả các dòng trong bảng
    for row in student_table.get_children():
        student_table.delete(row)

    # Kết nối đến cơ sở dữ liệu và lấy danh sách sinh viên
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT semester, class_code, subject_name, student_name, mssv, so_ngay_nghi FROM students")
    students = c.fetchall()
    conn.close()

    # Chèn các sinh viên vào bảng
    for student in students:
        student_table.insert("", "end", values=student)
