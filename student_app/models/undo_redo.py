import sqlite3

undo_stack = []
redo_stack = []

def save_state():
    """Lưu trạng thái hiện tại của bảng students vào undo_stack"""
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        current_state = c.fetchall()
        undo_stack.append(current_state)
        # Sau khi thao tác mới, redo sẽ bị xóa
        redo_stack.clear()

def restore_state(state):
    """Phục hồi một trạng thái students từ mảng dữ liệu"""
    with sqlite3.connect('data.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM students")
        for row in state:
            row = row[1:]  # Bỏ qua cột ID nếu có
            c.execute("""
                INSERT INTO students 
                (semester, class_code, subject_name, student_name, mssv, so_ngay_nghi, phan_tram_vang, thoi_gian_nghi)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", row)
        conn.commit()

def undo(app):
    if undo_stack:
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM students")
            current_state = c.fetchall()
        redo_stack.append(current_state)

        previous_state = undo_stack.pop()
        restore_state(previous_state)
        app.refresh_table()
        app.load_students()
    else:
        print("Không thể undo.")

def redo(app):
    if redo_stack:
        with sqlite3.connect('data.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM students")
            current_state = c.fetchall()
        undo_stack.append(current_state)

        next_state = redo_stack.pop()
        restore_state(next_state)
        app.refresh_table()
        app.load_students()
    else:
        print("Không thể redo.")
