# 📝 To-Do List Application

A modular, production-ready **Task & Project Management system** built using:

* **Python 3.13**
* **FastAPI** (REST API)
* **SQLAlchemy ORM**
* **Alembic** (database migrations)
* **PostgreSQL**
* **Poetry** (dependency + venv management)
* **Rich CLI** (optional)
* **Postman** (API testing, exported JSON collections included)

The project contains **both a CLI interface** and a **FastAPI server**, using clean architecture patterns:
`Services → Repositories → Database`.

---

## 🚀 Features

### ✅ Project Management

* Create, list, and delete projects
* Automatic timestamping (created / updated)

### ✅ Task Management

* Create tasks under projects
* Update status (`TODO`, `IN_PROGRESS`, `DONE`, `OVERDUE`)
* Automatic timestamp updates
* Validation of project existence
* Query tasks by:

  * project
  * status
  * task ID inside project

### ✅ API (FastAPI)

* Fully RESTful API for projects & tasks
* JSON responses
* Query filtering
* Error handling (custom exceptions)
* Swagger UI and ReDoc available automatically

### ✅ CLI

* Add projects
* Add tasks
* Mark tasks done
* View project/task lists
* Works directly from the terminal

---

## 📁 Project Structure

```
todolist/
│   main.py              # CLI entry point
│   api.py               # FastAPI entry point (optional)
│   pyproject.toml       
│   README.md
│
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── db/              # DB engine, session, base
│   ├── repositories/    # CRUD layer
│   ├── services/        # Business logic
│   ├── schemas/         # (Optional) Pydantic models for API
│   └── utils/           # Helpers
│
└── app2/                # Alembic directory
    ├── env.py
    ├── versions/        # Migration files
    └── script.py.mako
```

---

## 🛠 Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd todolist
```

### 2. Install dependencies (Poetry)

```
poetry install
```

### 3. Activate virtual environment

```
poetry shell
```

### 4. Create `.env`

```
DATABASE_URL=postgresql+psycopg2://user:*****@localhost:5433/todolist_db
```

---

## 🗄 Initialize Database

### Run migrations:

```
alembic upgrade head
```

### If you need to autogenerate future migrations:

```
alembic revision --autogenerate -m "Your message"
alembic upgrade head
```

---

## ▶ Running the CLI

Inside the virtual environment:

```
python main.py cli
```

Examples:

```
python main.py project create "School Work" "Assignments and deadlines"
python main.py task add 1 "Math HW" "Do exercises 1–10"
python main.py task list 1
python main.py task done 3
```

---

## 🌐 Running the API (FastAPI)

If your FastAPI entry file is **api.py**:

```
uvicorn api:app --reload
```

Then visit:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Postman Collection (Included)

Inside the repository, you will find:

```
postman/
    todolist_collection.postman_collection.json
    todolist_environment.postman_environment.json
```

Import both into Postman:

1. **Postman → Import → Upload Files**
2. Select the JSON files
3. You now have all GET/POST/PUT/DELETE tests ready to run

---

## 🧱 Technologies Used

| Component       | Tech            |
| --------------- | --------------- |
| Language        | Python 3.13     |
| Framework       | FastAPI         |
| ORM             | SQLAlchemy      |
| DB              | PostgreSQL      |
| Migrations      | Alembic         |
| Package Manager | Poetry          |
| Task Status     | Custom Enum     |
| API Testing     | Postman         |
| CLI             | Rich (optional) |

---

## 🚨 Common Issues & Fixes

### ❗ Enum mismatch:

If you get errors like:

```
invalid input value for enum taskstatus: "DOING"
```

Ensure your Python enum **matches PostgreSQL enum** and run migrations.

---

## 📌 Future Improvements

* JWT authentication (FastAPI Users)
* Docker deployment
* Task priority levels
* Notification scheduler
* User accounts & multi-tenancy

---

## 👤 Author

**Morteza Maddah**
Python / FastAPI Developer
Email: [maddahmasoud@gmail.com](mailto:maddahmasoud@gmail.com)

---

If you want, I can also generate:

✅ API documentation (OpenAPI examples)
✅ CLI usage table
✅ Entity-relationship diagram
✅ Badges (Poetry, FastAPI, PostgreSQL, etc.)
