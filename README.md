# student-management-system

> A desktop application for managing student information  
> Developed as a final project for the *Specialized Project* course (Đồ án chuyên ngành)

## 📌 Features

- Add, update, delete student records
- Import student data from Excel files
- Search and sort students by various fields
- Filter students by class and subject
- Undo/Redo support
- Send emails to students
- Persistent storage using SQLite
- GUI built with Tkinter

## 🧠 Technologies Used

- **Python 3**
- **Tkinter** for GUI
- **SQLite** for database
- **openpyxl / pandas** for Excel handling
- **smtplib** for sending emails

## 🗂️ Project Structure

project_root/
 │ ├── main.py # Entry point 
 ├── ui/ # UI components (buttons, layout...) 
 ├── models/ # Logic for data handling (CRUD, search, sort...) 
 ├── db/ # Database initialization and queries 
 ├── assets/ # Icons, images, Excel templates (optional) 
 └── README.md

 ## 🚀 Getting Started

1. **Install dependencies** (if not already):
   ```bash
   pip install pandas openpyxl

2. Run the app:
    ```
    python main.py

Note: This project does not require an internet connection, all data is saved locally in SQLite.
