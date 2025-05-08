# Student Management System

> A desktop application for managing student data imported from Excel files.  
> Developed as a personal project for the *Specialized Project* course.

## 📌 Features

- 🔐 User login and registration
- 📁 Import student data from Excel files
- 📋 Display student info in a table:
  - Semester
  - Class Code
  - Subject Name
  - Student Name
  - Student ID
  - Days Absent
- 🔍 Search and sort students
- ✏️ Edit and save student information
- ❌ Delete student entries
- 📧 Send warning emails to students with excessive absences
- 🤖 Chatbot integration for quick student information queries
- 💾 Data persistence with SQLite

## 💬 Chatbot Feature

The application now includes a **Chatbot** for quick student information lookup.  
The Chatbot uses **Hugging Face API** to generate SQL queries based on user input.  

💡 Using the Chatbot
- Click on the "Chat Bot" button in the application interface.

- Enter your query (e.g., "Sinh viên A nghỉ mấy ngày?") and click "Gửi".

- The chatbot will respond with the relevant information.

- Ensure your API key is correctly configured for the chatbot to function.

## 📁 Project Structure

```plaintext
project_root/
├── config/                # Configuration files (.env, version)
├── data/                  # Excel files for import
├── student_app/           # Main application package
│   ├── data_management/   # Data processing and transformation logic
│   ├── db/                # SQLite database access and operations
│   ├── models/            # Business logic: CRUD, search, sort, etc.
│   ├── ui/                # UI components: login, dashboard, buttons
│   └── utils/             # Helpers: import Excel, delete tables, send email, chatbot AI 
├── main.py                # Application entry point
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
```
## 🚀 Getting Started

1. **Create and activate a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   venv/Scripts/activate     # Windows
   ```
2. **Setup .env file for Chatbot**

    - Open the .env.example file.
    
    - Get your Hugging Face API Key [here](https://huggingface.co/settings/tokens).  
    
    - Add your API key to the file.
    - Rename the file to .env (remove .example) and save.
  
3. **Install dependencies**:

   ```
   pip install -r requirements.txt
4. **Run the application**:

   ```
   python main.py
📌 Notes:

- All data is stored locally using SQLite.

- Excel Format (for import)
Your Excel file should contain student information in the following format.
You can find example files in the data/ folder:
    - Example files: diem-danh-sinh-vien-04102024094447.xlsx
      
- The app works offline except for the chatbot feature.

- Make sure your API key is valid and active.

👨‍💻 Author
Nguyen Hong Phuc (Felix)
Student of Information Technology
