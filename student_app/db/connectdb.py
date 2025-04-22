import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Tạo bảng users nếu chưa tồn tại
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')

    # Tạo bảng students nếu chưa tồn tại
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 semester TEXT NOT NULL,
                 class_code TEXT NOT NULL,
                 subject_name TEXT NOT NULL,
                 student_name TEXT NOT NULL,
                 mssv TEXT NOT NULL,
                 so_ngay_nghi INTEGER NOT NULL DEFAULT 0,
                 phan_tram_vang INTEGER NOT NULL DEFAULT 0,
                 thoi_gian_nghi TEXT NOT NULL DEFAULT '')''')


    conn.commit()
    conn.close()