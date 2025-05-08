import tkinter as tk
from tkinter import ttk, Toplevel, Entry, Button, Text, Scrollbar, Frame, Label, Canvas, END
from student_app.models.undo_redo import redo, undo

class StudentAppUI:
    def __init__(self, root, logged_in_user, app):
        self.root = root
        self.logged_in_user = logged_in_user
        self.app = app  # Dùng để gọi hàm từ StudentApp

        self.root.title("Student Information System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Frame chứa các nút lớp học
        self.class_buttons_frame = tk.Frame(self.root, bg="#d9f9f9")
        self.class_buttons_frame.pack(fill=tk.X, pady=5)

        # Frame nhập
        self.info_frame = tk.Frame(self.root, bg="#95fce9")
        self.info_frame.pack(pady=10)

        tk.Label(self.info_frame, text="Thông Tin Sinh Viên", font=("Arial", 16), bg="#95fce9").grid(row=0, column=0, columnspan=6, pady=10)

        self.tools_button = tk.Button(self.root, text="Công Cụ", command=self.toggle, bg="#2196F3", fg="white")
        self.tools_button.place(x=10, y=10)

        self.tools_frame = tk.Frame(self.root)
        self.tools_frame.place(x=10, y=50)
        self.tools_frame.place_forget()

        self.import_button = tk.Button(self.tools_frame, text="Nhập file Excel", bg="#2196F3", command=self.app.import_excel, fg="black")
        self.import_button.grid(row=0, column=0, padx=5)

        self.clear_data_button = tk.Button(self.tools_frame, text="Xóa Tất Cả Dữ Liệu", bg="#f44336", command=self.app.relogin_and_clear_data, fg="white")
        self.clear_data_button.grid(row=1, column=0, padx=5)

        self.logout_button = tk.Button(self.tools_frame, text="Đăng xuất", bg="#FF5722", fg="white", command=self.app.logout)
        self.logout_button.grid(row=2, column=0, padx=5)

        self.semester_entry = self.create_input_field(self.info_frame, "Đợt:", 1, 0)
        self.class_code_entry = self.create_input_field(self.info_frame, "Mã Lớp:", 1, 2)
        self.subject_name_entry = self.create_input_field(self.info_frame, "Tên Môn Học:", 1, 4)
        self.mssv_entry = self.create_input_field(self.info_frame, "MSSV:", 2, 0)
        self.student_name_entry = self.create_input_field(self.info_frame, "Họ Tên Sinh Viên:", 2, 2, colspan=3)

        button_frame = tk.Frame(self.info_frame, bg="#95fce9")
        button_frame.grid(row=3, column=0, columnspan=6, pady=10)

        self.create_button(button_frame, "Lưu Thông Tin", self.app.save_info, 0, 0)
        self.create_button(button_frame, "Xóa", self.app.delete_student, 0, 1)
        self.create_button(button_frame, "Gửi mail", self.app.on_send_email, 0, 2)
        self.create_button(button_frame, "Làm Mới", self.app.refresh_table, 0, 3)
        self.create_button(button_frame, "↶ Hoàn tác", lambda: undo(self.app), 0, 4)
        self.create_button(button_frame, "↷ Làm lại", lambda: redo(self.app), 0, 5)
        self.create_button(self.info_frame, "Tìm Kiếm", self.app.search_students, 4, 4)

        self.search_entry = tk.Entry(self.info_frame, width=50)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=3)
        self.sort_button = self.create_sort_button(self.info_frame)
        self.sort_button = self.create_sort_button(self.info_frame)
        self.student_table = self.create_student_table()
        self.student_table.bind("<<TreeviewSelect>>", self.app.on_student_select)
        self.student_table.bind("<Double-1>", self.app.on_student_double_click)

        # Frame chatbot
        self.chatbot_button = tk.Button(self.root, text="Chat Bot", command=self.open_chatbot_window, bg="#4CAF50", fg="white")
        self.chatbot_button.place(x=1100, y=10)

    def open_chatbot_window(self):
        """Mở cửa sổ chatbot"""
        chatbot_window = Toplevel(self.root)
        chatbot_window.title("Chat Bot")
        chatbot_window.geometry("500x450")
        chatbot_window.configure(bg="#f0f0f0")

        # Main container frame
        main_frame = Frame(chatbot_window, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Chat display area with scrollbar
        chat_frame = Frame(main_frame, bg="#f0f0f0")
        chat_frame.pack(fill="both", expand=True)

        # Create canvas and scrollbar
        canvas = Canvas(chat_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#f0f0f0")

        # Configure scroll region
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.chat_display = scrollable_frame

        # Input area
        input_frame = Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill="x", pady=(10, 0))

        self.chat_entry = Entry(input_frame, font=("Arial", 12))
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.chat_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = Button(input_frame, text="Gửi", bg="#4CAF50", fg="white",
                                font=("Arial", 12, "bold"), command=self.send_message)
        self.send_button.pack(side="right")

    def send_message(self):
        question = self.chat_entry.get()
        if question:
            self.display_message(question, "user")
            self.chat_entry.delete(0, END)
            
            response = self.app.ask_chatbot(question)
            self.display_message(response, "bot")

    def display_message(self, message, sender):
        """Hiển thị tin nhắn theo kiểu Messenger với căn chỉnh tối ưu"""
        # Tạo container chứa tin nhắn
        container = Frame(self.chat_display, bg="#f0f0f0")
        container.pack(fill="x", pady=2)
        
        # Xác định màu sắc và vị trí
        if sender == "user":
            bubble_color = "#0084FF"
            text_color = "white"
            pack_side = "right"
            padx = (70, 10)
            anchor = "ne"
        else:
            bubble_color = "#E4E6EB"
            text_color = "black"
            pack_side = "left"
            # Giảm padding phải để đẩy sát lề trái
            padx = (10, 200)  # Giá trị 200 có thể điều chỉnh tùy nhu cầu
            anchor = "nw"  # Neo góc trái trên
        
        # Tạo bong bóng tin nhắn với kích thước tự nhiên
        bubble = Frame(container, bg=bubble_color, padx=12, pady=8)
        bubble.pack(side=pack_side, padx=padx, anchor=anchor)
        
        # Thêm nội dung tin nhắn
        Label(
            bubble,
            text=message,
            font=("Arial", 12),
            wraplength=300,
            justify="left",
            bg=bubble_color,
            fg=text_color,
            bd=0
        ).pack()
        
        # Cập nhật giao diện ngay lập tức
        container.update_idletasks()
        
        # Cuộn xuống dưới cùng
        canvas = container.master.master
        canvas.yview_moveto(1.0)

    def create_input_field(self, parent, label_text, row, column, colspan=1):
        tk.Label(parent, text=label_text, bg="#95fce9").grid(row=row, column=column, padx=5, pady=5)
        entry = tk.Entry(parent, width=20)
        entry.grid(row=row, column=column+1, padx=5, pady=5, columnspan=colspan)
        return entry

    def create_button(self, parent, text, command, row, column):
        tk.Button(parent, text=text, command=command, bg="#55f2ed", fg="black").grid(row=row, column=column, padx=5)

    def create_sort_button(self, parent):
        sort_button = tk.Menubutton(parent, text="Sắp Xếp", relief=tk.RAISED, bg="#FF9800", fg="white")
        sort_menu = tk.Menu(sort_button, tearoff=0)
        sort_button["menu"] = sort_menu

        sort_menu.add_command(label="Tên (A -> Z)", command=lambda: self.app.sort_students("student_name", True))
        sort_menu.add_command(label="Tên (Z -> A)", command=lambda: self.app.sort_students("student_name", False))
        sort_menu.add_command(label="Số ngày nghỉ (Tăng)", command=lambda: self.app.sort_students("so_ngay_nghi", True))
        sort_menu.add_command(label="Số ngày nghỉ (Giảm)", command=lambda: self.app.sort_students("so_ngay_nghi", False))
        sort_menu.add_command(label="Mã lớp", command=lambda: self.app.sort_students("class_code", True))
        sort_menu.add_command(label="Môn học", command=lambda: self.app.sort_students("subject_name", True))

        sort_button.grid(row=4, column=5, padx=5, pady=10)
        return sort_button

    def create_student_table(self):
        table = ttk.Treeview(self.root, columns=("semester", "class_code", "subject_name", "student_name", "mssv", "so_ngay_nghi"), show="headings")
        table.heading("semester", text="Đợt")
        table.heading("class_code", text="Mã Lớp")
        table.heading("subject_name", text="Tên Môn Học")
        table.heading("student_name", text="Họ Tên SV")
        table.heading("mssv", text="MSSV")
        table.heading("so_ngay_nghi", text="Số ngày nghỉ")

        table.column("semester", width=100)
        table.column("class_code", width=100)
        table.column("subject_name", width=200)
        table.column("student_name", width=250)
        table.column("mssv", width=100)
        table.column("so_ngay_nghi", width=100)

        table.pack(fill=tk.BOTH, expand=True)
        return table

    def toggle(self):
        if self.tools_frame.winfo_ismapped():
            self.tools_frame.place_forget()
        else:
            self.tools_frame.place(x=10, y=50)

    def create_class_button(self, table_key):
        """Tạo nút động cho từng lớp"""
        button = tk.Button(self.class_buttons_frame, text=table_key, command=lambda: self.app.switch_table(table_key), bg="#4CAF50", fg="white")
        button.pack(side=tk.LEFT, padx=5, pady=5)

    def update_table(self, data):
        """Cập nhật dữ liệu bảng"""
        for row in self.student_table.get_children():
            self.student_table.delete(row)
        for row in data:
            self.student_table.insert("", tk.END, values=row)
