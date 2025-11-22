# 📝 ToDoList CLI Project

A simple **project and task management system** built with Python.  
This version is fully **in-memory (no database, no API)** and runs through a **Command-Line Interface (CLI)**.

---

## ⚙️ Features

✅ **Project Management**
- Create a new project  
- Edit project name and description  
- Delete a project (with automatic cascade delete for its tasks)  
- List all existing projects  

✅ **Task Management**
- Add new tasks to a project  
- Edit title, description, status, and deadline  
- Delete a task  
- Change task status (`todo` / `doing` / `done`)  
- View all tasks for a specific project  

---

## 🧠 Project Structure

todolist_core/
├── app/
│ ├── init.py ← main logic class: ToDoManager
│ ├── models.py ← defines Project and Task classes
│ ├── crud.py ← CRUD operations for projects and tasks
│ ├── config.py ← configuration values (e.g., VALID_STATUSES)
│ ├── utils.py ← helper functions (validation, limits, etc.)
│
├── menu.py ← CLI user interface
├── main.py ← entry point of the program
├── .env.example ← sample environment configuration
└── README.md ← project documentation

yaml
Copy code

---

## 🚀 Running the Program

### 1️⃣ Check Python Installation
Make sure **Python 3.10+** is installed.
Also install pipx to work on poetry

```bash
python --version
2️⃣ Run the Project
Run the following command from the project root:

bash
Copy code
python main.py
📟 Example Output:

🚀 ToDoList Management System Ready.

📋 ToDoList Menu
1️⃣ Create Project
2️⃣ Edit Project
3️⃣ Delete Project
4️⃣ View All Projects
5️⃣ Add Task
6️⃣ Edit Task
7️⃣ Delete Task
8️⃣ Change Task Status
9️⃣ View Tasks in Project
0️⃣ Exit
👉 Your choice:
⚙️ Environment Configuration (.env)
The .env file defines limits and app settings.
A sample configuration file is provided as .env.example:

ini
Copy code
MAX_NUMBER_OF_PROJECT=5
MAX_NUMBER_OF_TASK=10
⚠️ The real .env file should not be committed to version control for security and configurability reasons. ⚠️

🔁 Cascade Delete
Each project acts as a container for its tasks.
When a project is deleted, all its associated tasks are automatically removed
to prevent orphaned data and maintain data consistency.

💡 Valid Task Statuses
Tasks can only have one of the following statuses:

bash
Copy code
todo | doing | done
If an invalid value is provided, a ValueError will be raised.

🧩 Development Workflow
Recommended Git branching workflow:

Create new feature branches from develop (e.g., feature/add-task-deadline)

Commit and test changes

Merge back into develop

Only stable, production-ready versions should be merged into main

🧰 Technologies Used
Tool Description
🐍 Python Main programming language
🧩 dotenv Loads environment variables from .env
🧠 OOP Object-Oriented design for managing projects and tasks
🖥 CLI Command Line Interface for user interaction

👤 Author
Name: Morteza Maddah

Date: October 2025


💬 Future Improvements

Save data to a JSON file

Add a graphical interface (maybe tkinter)

Build a REST API using FastAPI


