import sqlite3

def search_students(app):
    """Tìm kiếm sinh viên theo tên hoặc MSSV."""
    # Lấy giá trị từ ô tìm kiếm (search_entry) trong UI
    search_term = app.ui.search_entry.get().strip()

    # Xóa tất cả các dòng trong bảng sinh viên (student_table)
    for row in app.ui.student_table.get_children():  # Sử dụng app.ui để truy cập student_table
        app.ui.student_table.delete(row)

    # Kết nối đến cơ sở dữ liệu và thực hiện truy vấn
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Truy vấn tìm kiếm sinh viên theo MSSV hoặc tên
    c.execute("""
        SELECT semester, class_code, subject_name, student_name, mssv, so_ngay_nghi 
        FROM students 
        WHERE mssv LIKE ? OR student_name LIKE ?
    """, (f"%{search_term}%", f"%{search_term}%"))

    # Lấy kết quả trả về
    students = c.fetchall()
    conn.close()

    # Thêm sinh viên vào bảng
    for student in students:
        app.ui.student_table.insert("", "end", values=student)  # Sử dụng app.ui để truy cập student_table

def sort_students(app, column, ascending):
    """Sắp xếp các sinh viên theo cột được chỉ định."""
    if column == "student_name":
        # Sắp xếp theo tên (lấy phần tên cuối cùng trong họ tên đầy đủ)
        data = [(get_last_name(app.ui.student_table.set(child, column)), 
                 app.ui.student_table.set(child, column), child) for child in app.ui.student_table.get_children('')]
        data.sort(reverse=not ascending)  # Sắp xếp ngược nếu không tăng dần
        for index, (_, _, child) in enumerate(data):
            app.ui.student_table.move(child, '', index)
    elif column in ["class_code", "subject_name"]:
        # Sắp xếp theo mã lớp hoặc tên môn học
        data = [(app.ui.student_table.set(child, column), child) for child in app.ui.student_table.get_children('')]
        data.sort(reverse=not ascending)  # Sắp xếp ngược nếu không tăng dần
        for index, (_, child) in enumerate(data):
            app.ui.student_table.move(child, '', index)
    else:
        # Sắp xếp cho các cột khác
        data = [(app.ui.student_table.set(child, column), child) for child in app.ui.student_table.get_children('')]
        # Nếu là cột "so_ngay_nghi", chuyển sang float để so sánh, nếu không thì sắp xếp chuỗi
        if column == "so_ngay_nghi":
            data.sort(key=lambda x: float(x[0]), reverse=not ascending)
        else:
            data.sort(reverse=not ascending)
        for index, (_, child) in enumerate(data):
            app.ui.student_table.move(child, '', index)

def get_last_name(full_name):
    """Lấy phần tên cuối cùng trong họ tên đầy đủ."""
    return full_name.split()[-1]
