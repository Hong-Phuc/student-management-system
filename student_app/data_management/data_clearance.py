# clear_data.py
import sqlite3
import tkinter as tk
from tkinter import messagebox

def clear_all_students(app):
    """Xóa sạch toàn bộ dữ liệu trong bảng students."""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # Xóa tất cả dữ liệu trong bảng
    c.execute("DELETE FROM students")

    conn.commit()
    conn.close()

    # Cập nhật lại giao diện
    app.load_students()  
    messagebox.showinfo("Clear Data", "Tất cả dữ liệu đã được xóa!")

def relogin_and_clear_data(app):
    """Yêu cầu người dùng đăng nhập lại trước khi xóa tất cả dữ liệu."""
    relogin_window = tk.Toplevel(app.root)
    relogin_window.title("Bạn cần phải đăng nhập lại để thực hiện thao tác này !")
    relogin_window.geometry("500x200")

    # Tạo ô nhập cho tên người dùng
    tk.Label(relogin_window, text="Username").pack(pady=5)
    relogin_username_entry = tk.Entry(relogin_window)
    relogin_username_entry.pack(pady=5)

    # Tạo ô nhập cho mật khẩu
    tk.Label(relogin_window, text="Password").pack(pady=5)
    relogin_password_entry = tk.Entry(relogin_window, show="*")
    relogin_password_entry.pack(pady=5)

    # Xác nhận đăng nhập lại
    def confirm_login():
        username = relogin_username_entry.get()
        password = relogin_password_entry.get()

        # Kiểm tra xem tên đăng nhập có khớp với tài khoản ban đầu không
        if username != app.logged_in_user:
            messagebox.showerror("Login Error", "Bạn phải đăng nhập lại bằng tài khoản đã đăng nhập ban đầu.")
            return

        # Kiểm tra thông tin đăng nhập trong cơ sở dữ liệu
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            clear_all_students(app)  # Xóa tất cả dữ liệu nếu đăng nhập thành công
            relogin_window.destroy()
        else:
            messagebox.showerror("Login Error", "Sai mật khẩu.")

    # Nút xác nhận và hủy
    tk.Button(relogin_window, text="Confirm", command=confirm_login, bg='red', fg='white').pack(pady=10)
    tk.Button(relogin_window, text="Cancel", command=relogin_window.destroy, bg='#0ffa46', fg='black').pack(pady=5)
