# AI-First CRM HCP Module

## Overview
This project is an AI-first Customer Relationship Management (CRM) system for Healthcare Professionals (HCPs). It features a "Log Interaction Screen" allowing field representatives to log interactions via a structured form or conversational chat interface.

The application leverages LangGraph and Groq's gemma2-9b-it model to intelligently manage HCP interactions through an AI Assistant.

## Tech Stack
*   **Frontend**: React, Redux Toolkit, Tailwind CSS, Lucide React
*   **Backend**: Python, FastAPI, SQLAlchemy, LangGraph, Groq (gemma2-9b-it)
*   **Database**: SQLite (Development) / PostgreSQL (Production)

## Features
*   **Dual Logging Interfaces**: Log interactions using a comprehensive structured form or naturally via the AI chat interface.
*   **AI Agent Workflow (LangGraph)**:
    *   **Log Interaction**: Extracts structured data from conversational input.
    *   **Edit Interaction**: Allows natural language modifications to logged data.
    *   **HCP Insights**: Retrieves interaction history for specific doctors.
    *   **Suggest Follow-up**: Recommends next best actions based on context.
    *   **Summary**: Summarizes recent interactions.

## Prerequisites
*   Node.js (v18+)
*   Python (3.9+)
*   Groq API Key

## Setup & Running Locally

### Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment Variables:
    *   Update `.env` file in the `backend` directory. Add your `GROQ_API_KEY`.
5.  Run the backend server using uvicorn:
    ```bash
    uvicorn src.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

# crm-hcp-ai
