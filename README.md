# ✅ TaskBOT - AI-Powered Task Management Assistant

TaskBOT is an AI-powered task management application built with **Streamlit**, **LangGraph**, **LangChain**, **Groq**, and **SQLite**. It allows users to create, view, update, and delete tasks using natural language conversations.

## 🚀 Features

* 🤖 AI-powered task management using Groq LLM
* 📋 Create new tasks with natural language
* 🔍 View and filter tasks
* ✏️ Update task status (pending, in_progress, completed)
* 🗑️ Delete tasks
* 💾 SQLite database for persistent storage
* 🧠 Conversational memory using LangGraph
* 🎨 Modern and responsive Streamlit UI

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangGraph
* LangChain
* Groq
* SQLite
* SQLDatabase Toolkit

---

## 📂 Project Structure

```bash
TaskBOT/
│
├── app.py
├── style.css
├── my_task.db
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/TaskBOT.git
cd TaskBOT
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from Groq Console.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 💬 Example Commands

### Create Task

```text
Create a task called Complete React Project
```

### View Tasks

```text
Show all tasks
```

### Update Task

```text
Mark task 3 as completed
```

### Delete Task

```text
Delete task 2
```

### Filter Tasks

```text
Show all pending tasks
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('pending','in_progress','completed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🧠 How It Works

1. User enters a task-related request.
2. LangGraph Agent interprets the request.
3. SQLDatabase Toolkit generates SQL queries.
4. SQLite database executes CRUD operations.
5. Results are returned in a conversational format.

---

## 📸 Preview

TaskBOT provides a clean chat-based interface where users can manage tasks through natural language instead of manually interacting with databases.

---

## Future Enhancements

* User authentication
* Due dates and reminders
* Task priorities
* Multi-user support
* Cloud database integration
* Task analytics dashboard

---

## 📜 License

This project is open-source and available under the MIT License.

---

### Author

**Vivek Singh**

GitHub: https://github.com/vivek-singh98

Built with ❤️ using LangGraph, LangChain, Groq, Streamlit, and SQLite.
