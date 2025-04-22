import tkinter as tk
from tkinter import messagebox

# Các module
from student_app.db.connectdb import init_db

from student_app.models.login_register import LoginRegisterApp
from student_app.models.load_table import load_students
from student_app.models.add_student import save_info
from student_app.models.search_sort import search_students, sort_students, get_last_name
from student_app.models.select_student import get_selected_student, on_student_select, on_student_double_click
from student_app.models.delete_student import delete_student
from student_app.models.undo_redo import undo, redo


from student_app.data_management.data_clearance import relogin_and_clear_data, clear_all_students

from student_app.utils.excel_import import import_excel, extract_subject_name
from student_app.utils.send_email import on_send_email
from student_app.utils.delete_all_table import refresh_table

from student_app.ui.ui import StudentAppUI

class StudentApp:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.ui = StudentAppUI(root, logged_in_user, self)

        self.load_students()

    def logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.root.destroy()
            new_root = tk.Tk()
            LoginRegisterApp(new_root, StudentApp)
            new_root.mainloop()

    def import_excel(self):
        import_excel(self)

    def sort_students(self, column, ascending=True):
        sort_students(self, column, ascending)

    def get_last_name(self):
        return get_last_name(self)

    def load_students(self):
        load_students(self.ui.student_table)

    def extract_subject_name(self):
        return extract_subject_name(self)

    def relogin_and_clear_data(self):
        relogin_and_clear_data(self)

    def clear_all_students(self):
        clear_all_students(self)

    def save_info(self):
        save_info(self)

    def delete_student(self):
        delete_student(self)

    def on_send_email(self):
        on_send_email()

    def undo(self):
        undo(self)

    def redo(self):
        redo(self)

    def search_students(self):
        search_students(self)

    def refresh_table(self):
        refresh_table(self)

    def get_selected_student(self):
        return get_selected_student(self.ui.student_table)

    def on_student_select(self, event):
        on_student_select(self, event)

    def on_student_double_click(self, event):
        on_student_double_click(self, event)


if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    LoginRegisterApp(root, StudentApp)
    root.mainloop()
