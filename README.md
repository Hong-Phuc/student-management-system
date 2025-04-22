# Student Management System

> A desktop application for managing student data imported from Excel files.  
> Developed as a personal project for the *Specialized Project* course.

## 📌 Features

- 🔐 User login and registration
- 📁 Import student data from Excel files
- 📋 Display student info in a table:
  - Full name
  - Class
  - Days absent
  - Class ID
  - Student ID
- 🔍 Search and sort students
- ✏️ Edit and save student information
- ❌ Delete student entries
- 📧 Send warning emails to students with excessive absences
- 💾 Data persistence with SQLite

## 🗂️ Project Structure

project_root/ │ ├── main.py # Entry point ├── ui/ # UI components (login, main screen, buttons) ├── models/ # Business logic: CRUD, search, sort, etc. ├── db/ # SQLite database logic ├── data/ # Excel files used for import ├── requirements.txt └── README.md

markdown
Copy
Edit

## 🚀 Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   
2. Run the application:
   ```
   python main.py
Note:

All data is stored locally using SQLite

The data/ folder contains example Excel files

The app works offline

✅ Excel Format (for import)
Your Excel file should contain student information in the following format.  
You can find example files in the `data/` folder:
### Example files:
`diem-danh-sinh-vien-04102024094447.xlsx`

👨‍💻 Author
Nguyen Hong Phuc (Felix)
Student of Information Technology
