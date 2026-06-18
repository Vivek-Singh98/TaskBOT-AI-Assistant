from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="TaskBOT",
    page_icon="✅",
    layout="centered"
)

# ── Load CSS ─────────────────────────────────────────────
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Database Setup ────────────────────────────────────────
db = SQLDatabase.from_uri("sqlite:///my_task.db")

db.run("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT CHECK(status IN ('pending','in_progress', 'completed')) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

# ── LLM , tools , memory , system_prompt ─────────────────
llm = ChatGroq(model="openai/gpt-oss-20b")

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table. You can perform CRUD operations based on user instructions.

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured markdown table format that is clean, readable, and includes all relevant columns.
4. Always use proper markdown table with headers: | ID | Title | Description | Status | Created At |

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR title=?

Table schema: id, title, description, status(pending/in_progress/completed), created_at.
"""


@st.cache_resource
def get_agent():
    agent = create_agent(
        model=llm,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent


agent = get_agent()

# ── UI Header ─────────────────────────────────────────────
st.markdown("""
<div class="taskbot-header">
    <h1>✅ Task<span>BOT</span></h1>
    <p>AI-powered task manager · Powered by Groq + LangGraph</p>
</div>
""", unsafe_allow_html=True)

# ── Suggestion Chips ──────────────────────────────────────
st.markdown("""
<div class="suggestion-chips">
    <span class="chip">📋 Show all tasks</span>
    <span class="chip">➕ Add a new task</span>
    <span class="chip">✅ Mark task completed</span>
    <span class="chip">🗑️ Delete a task</span>
    <span class="chip">🔄 Update status</span>
</div>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Empty State ───────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🗂️</div>
        <p>No conversation yet. Ask me to create, view, update, or delete your tasks!</p>
    </div>
    """, unsafe_allow_html=True)

# ── Render Chat History ───────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat Input ────────────────────────────────────────────
prompt = st.chat_input("Ask me to manage your tasks... e.g. 'Show all pending tasks'")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            response = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                {"configurable": {"thread_id": "1"}}
            )

            result = response["messages"][-1].content
            st.markdown(result)
            st.session_state.messages.append({"role": "ai", "content": result})