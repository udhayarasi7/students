# 🎓 Student Database Management System with AI Agent

An intelligent, full-stack Student Management System powered by **FastAPI**, **LangGraph**, **Groq API (Llama 3)**, **SQLAlchemy (SQLite)**, and **ChromaDB**. The system utilizes a dual-retrieval AI agent capable of querying structured database records alongside unstructured vector embeddings, packaged seamlessly inside **Docker**.

---

## 🌟 Key Features

- **Dual Retrieval Engine**:
  - **Structured Queries (SQL)**: Queries SQLite via SQLAlchemy for specific database fields (GPA, Department, Enrollment Status).
  - **Unstructured Queries (Vector Search)**: Queries ChromaDB for semantic search over student profiles, hobbies, and interests.
- **LangGraph AI Agent**: Dynamically routes user prompts from `index.html` to either SQL execution or Vector similarity search using Groq LLM.
- **Containerized Architecture**: Single-command deployment using Docker & Docker Compose.
- **RESTful API**: Documented interactive endpoints via FastAPI (`/docs`).
- **Interactive UI**: Built-in Web Portal for chatting with the database agent.

---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI (Python 3.10)
- **AI Agent Framework**: LangGraph, LangChain
- **LLM Provider**: Groq API (`llama-3.3-70b-versatile`)
- **Databases**:
  - **Relational**: SQLite + SQLAlchemy ORM
  - **Vector DB**: ChromaDB
- **Containerization**: Docker & Docker Compose
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)

---

## 🚀 Quick Start with Docker

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Git](https://git-scm.com/) installed.

### 2. Clone Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Build and Run Container
```bash
docker compose up --build
```

Access the application in your browser:
- **Interactive Chat UI**: `http://localhost:8000`
- **Swagger API Docs**: `http://localhost:8000/docs`

---

## 📁 Project Structure

```text
student_system/
├── app/
├── ├── api/            # API Route handlers (Students & Chatbot)
├── ├── core/           # Configuration & DB connection settings
├── ├── models/         # SQLAlchemy ORM models
├── ├── schemas/        # Pydantic validation schemas
├── ├── services/       # LangGraph Agent & Vector Search logic
├── └── main.py          # FastAPI application entry point
├── docker-compose.yml  # Docker multi-container setup
├── Dockerfile          # App container configuration
├── index.html          # Web UI dashboard
├── requirements.txt    # Python dependencies
└── seed.py             # Database initialization script
```

---

## 🔒 Security
Sensitivite files (`.env`, local `.db` files, vector stores `chroma_db/`, and virtual environments) are intentionally excluded via `.gitignore` to prevent secret leaks.