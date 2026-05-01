"""
FastAPI routes for the CRM HCP Module.

Endpoints:
  POST  /interaction/log          — Structured form: directly insert an interaction
  PUT   /interaction/{id}         — Edit an existing interaction by ID
  DELETE /interaction/{id}        — Delete an interaction by ID
  GET   /interactions             — List all interactions (with optional filters)
  GET   /interaction/{id}         — Get a single interaction
  POST  /chat                     — Conversational AI: route through LangGraph agent
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from src.schemas.schemas import (
    InteractionCreate,
    InteractionUpdate,
    InteractionOut,
    ChatRequest,
    SuggestRequest,
)
from src.models.models import Interaction
from src.utils.database import get_db
from src.agent.agent import run_agent
from src.agent.tool import suggest_followup_tool

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /interaction/log — Structured form submission
# ---------------------------------------------------------------------------
@router.post("/interaction/log", response_model=InteractionOut, status_code=201)
def log_interaction(data: InteractionCreate, db: Session = Depends(get_db)):
    """
    Log a new HCP interaction via the structured form.
    Directly writes to the database — no AI processing needed.
    """
    interaction = Interaction(**data.model_dump())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


# ---------------------------------------------------------------------------
# PUT /interaction/{id} — Edit an existing interaction
# ---------------------------------------------------------------------------
@router.put("/interaction/{interaction_id}", response_model=InteractionOut)
def edit_interaction(
    interaction_id: int,
    data: InteractionUpdate,
    db: Session = Depends(get_db),
):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail=f"Interaction {interaction_id} not found")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)
    return interaction


# ---------------------------------------------------------------------------
# DELETE /interaction/{id} — Remove an interaction
# ---------------------------------------------------------------------------
@router.delete("/interaction/{interaction_id}", status_code=204)
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail=f"Interaction {interaction_id} not found")
    db.delete(interaction)
    db.commit()


# ---------------------------------------------------------------------------
# GET /interactions — List all (optional filter by doctor_name)
# ---------------------------------------------------------------------------
@router.get("/interactions", response_model=List[InteractionOut])
def get_all_interactions(
    doctor_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Interaction)
    if doctor_name:
        query = query.filter(Interaction.doctor_name.ilike(f"%{doctor_name}%"))
    return query.order_by(Interaction.created_at.desc()).all()


# ---------------------------------------------------------------------------
# GET /interaction/{id} — Single interaction detail
# ---------------------------------------------------------------------------
@router.get("/interaction/{interaction_id}", response_model=InteractionOut)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail=f"Interaction {interaction_id} not found")
    return interaction


# ---------------------------------------------------------------------------
# POST /chat — Conversational AI (LangGraph agent)
# ---------------------------------------------------------------------------
@router.post("/chat")
def chat(data: ChatRequest):
    """
    Conversational interface: send a free-text message and the LangGraph agent
    will decide which tool to call (log, edit, insights, suggest, summary).
    """
    result = run_agent(data.message)
    return {"response": result}


# ---------------------------------------------------------------------------
# POST /interaction/suggest_followup — Dynamic follow-up suggestion
# ---------------------------------------------------------------------------
@router.post("/interaction/suggest_followup")
def suggest_followup(data: SuggestRequest):
    """
    Directly requests a follow-up suggestion based on interaction context.
    """
    result = suggest_followup_tool(data.context)
    return result