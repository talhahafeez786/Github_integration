# 🚀 GitHub Integration API with FastAPI & MongoDB

This project is a backend API built using **FastAPI** and **MongoDB** that allows users to:
- Authenticate with GitHub via OAuth2
- Fetch and store GitHub data (repos, commits, issues, changelogs, organizations, users)
- Interact with the data through dynamic endpoints
- Perform global search across all GitHub data collections

---

## 📦 Project Setup

### ✅ 1. Clone the Repository
```bash
git clone https://github.com/talhahafeez786/Github_integration.git
cd Github-integration
```

### ✅ 2. Create and Activate Virtual Environment
#### For Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### For Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### ✅ 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Application

### ✅ Navigate to the `src` directory and start the FastAPI server:
```bash
cd src
uvicorn server:app --reload
```

---

## 📘 API Documentation

Once the server is running, visit:
```
http://localhost:8000/docs
```

This opens the **Swagger UI** where you can test all endpoints interactively.

