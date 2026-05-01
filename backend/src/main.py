from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ⚠️ Load .env BEFORE importing any internal modules that depend on env vars
load_dotenv()

from src.routes.routes import router
from src.models.models import Base
from src.utils.database import engine

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM — HCP Module",
    description=(
        "A pharmaceutical CRM backend with a LangGraph AI agent "
        "supporting both structured form and conversational interaction logging."
    ),
    version="1.0.0",
)

# Allow all origins during development — tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "CRM HCP API is running"}