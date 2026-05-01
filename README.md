# 🏥 CRM AI — AI-First CRM for Healthcare Professionals



## 📌 Overview

**CRM AI** is an AI-first CRM system designed for managing Healthcare Professional (HCP) interactions. It empowers field representatives to log, manage, and analyze doctor visits using both:

- 🧾 **Structured forms** — traditional manual entry
- 🤖 **Conversational AI** — natural language chat interface

Powered by **LangGraph** multi-agent workflows and **Groq (gemma2-9b-it)** for blazing-fast AI inference.

---

## 🧠 Features

### 🔹 Dual Logging Interface
- Manual form-based interaction logging
- AI chat-based logging via natural language

### 🔹 AI Agent Workflows (LangGraph)

| Workflow | Description |
|---|---|
| 📝 **Log Interaction** | Extracts structured data from free-text chat |
| ✏️ **Edit Interaction** | Modifies existing logs using natural language |
| 📊 **HCP Insights** | Fetches and presents doctor interaction history |
| 🔮 **Follow-up Suggestions** | Recommends next best actions for each HCP |
| 🧠 **Summarization** | Summarizes recent interactions for quick review |

---

## 🏗️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Redux Toolkit, Tailwind CSS, Lucide React |
| **Backend** | Python, FastAPI, SQLAlchemy, LangGraph |
| **AI / LLM** | Groq API (`gemma2-9b-it`) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |

---

## 📦 Prerequisites

Make sure you have the following installed:

- [Node.js](https://nodejs.org/) v18+
- [Python](https://www.python.org/) 3.9+
- A valid [Groq API Key](https://console.groq.com/)

---

## ⚙️ Setup & Installation

### 🔧 Backend Setup

**1. Navigate to the backend folder**
```bash
cd backend
```

**2. Create a virtual environment**

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file inside the `backend/` directory:
```env
GROQ_API_KEY=your_api_key_here
```

**5. Start the backend server**
```bash
uvicorn src.main:app --reload
```

Backend runs at 👉 **http://localhost:8000**

---

### 🎨 Frontend Setup

**1. Navigate to the frontend folder**
```bash
cd frontend
```

**2. Install dependencies**
```bash
npm install
```

**3. Start the development server**
```bash
npm run dev
```

Frontend runs at 👉 **http://localhost:5173**

---

## 🔗 API Documentation

Interactive Swagger UI available at 👉 **http://localhost:8000/docs**

### 🧪 Sample API Call

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Met Dr Sharma at AIIMS, discussed insulin and follow up next week"
  }'
```

---

## 📂 Project Structure

```
crm-hcp-ai/
│
├── backend/
│   ├── src/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routes/               # API route handlers
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── services/             # Business logic layer
│   │   └── agents/               # LangGraph AI workflows
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Page-level views
│   │   ├── redux/                # Redux Toolkit store & slices
│   │   └── services/             # API service layer
│   └── package.json
│
└── README.md
```

---

## 🚀 Future Enhancements

- [ ] 🔐 Role-based authentication (Admin / Rep)
- [ ] 📍 Location tracking for field visits
- [ ] 📈 Analytics dashboard (HCP engagement trends)
- [ ] 📅 Calendar & reminders integration
- [ ] 🎤 Voice-to-text interaction logging
- [ ] 🧠 Fine-tuned healthcare-specific LLM

---

## 💡 Why This Project Matters

- ✅ Demonstrates **AI-first product thinking**
- ✅ Uses **LangGraph** for multi-step agent reasoning
- ✅ Converts **natural language → structured CRM data**
- ✅ Solves a real **pharma industry use case**
- ✅ Designed as a scalable, production-grade SaaS concept

---

## 👨‍💻 Author

**Shivansh Saxena**
Full Stack Developer | MERN + AI



