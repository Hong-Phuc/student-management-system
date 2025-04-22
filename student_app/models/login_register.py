import sqlite3
import tkinter as tk
from tkinter import messagebox

class LoginRegisterApp:
    def __init__(self, root, student_app_class):
        self.root = root
        self.student_app_class = student_app_class
        self.root.title("Quản lý sinh viên")
        self.root.geometry("400x300")  # Tăng kích thước cửa sổ
        self.root.configure(bg="#f0f0f0")  # Màu nền nhẹ nhàng
        self.logged_in_user = None  # Biến lưu trữ người dùng đã đăng nhập

        # Màn hình đăng nhập/đăng ký
        self.login_screen()

    def login_screen(self):
        """Màn hình đăng nhập"""
        self.clear_screen()

        # Tiêu đề
        title_label = tk.Label(self.root, text="WELCOME!", font=("Arial", 18), bg="#f0f0f0")
        title_label.pack(pady=20)

        tk.Label(self.root, text="Username", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(self.root, text="Password", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5, padx=20, fill=tk.X)

        # Nút Đăng Nhập
        login_button = tk.Button(self.root, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Arial", 12))
        login_button.pack(pady=10, padx=20, fill=tk.X)

        # Nút Đăng Ký
        register_button = tk.Button(self.root, text="Register", command=self.register_screen, bg="#008CBA", fg="white", font=("Arial", 12))
        register_button.pack(pady=5, padx=20, fill=tk.X)

    def register_screen(self):
        """Màn hình đăng ký"""
        self.clear_screen()

        title_label = tk.Label(self.root, text="Create an Account", font=("Arial", 18), bg="#f0f0f0")
        title_label.pack(pady=20)

        tk.Label(self.root, text="Create Username", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.new_username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.new_username_entry.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(self.root, text="Create Password", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
        self.new_password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.new_password_entry.pack(pady=5, padx=20, fill=tk.X)

        register_button = tk.Button(self.root, text="Register", command=self.register, bg="#4CAF50", fg="white", font=("Arial", 12))
        register_button.pack(pady=10, padx=20, fill=tk.X)

        back_button = tk.Button(self.root, text="Back to Login", command=self.login_screen, bg="#f44336", fg="white", font=("Arial", 12))
        back_button.pack(pady=5, padx=20, fill=tk.X)

    def clear_screen(self):
        """Xóa các widget trên màn hình"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        """Hàm xử lý đăng nhập"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("", "Đăng nhập thành công!")
            self.logged_in_user = username
            self.show_student_info_screen()  # Chuyển sang giao diện quản lý sinh viên
        else:
            messagebox.showerror("", "Sai tài khoản hoặc mật khẩu.")

    def register(self):
        """Hàm xử lý đăng ký tài khoản mới"""
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if new_username and new_password:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
                conn.commit()
                messagebox.showinfo("", "Đăng ký thành công!")
                self.login_screen()  # Quay lại màn hình đăng nhập
            except sqlite3.IntegrityError:
                messagebox.showerror("", "Username đã tồn tại.")
            finally:
                conn.close()
        else:
            messagebox.showerror("", "Vui lòng điền đủ thông tin.")

    def show_student_info_screen(self):
        """Hiển thị giao diện quản lý sinh viên sau khi đăng nhập thành công"""
        self.clear_screen()
        self.student_app_class(self.root, self.logged_in_user)  # Sử dụng student_app_class


