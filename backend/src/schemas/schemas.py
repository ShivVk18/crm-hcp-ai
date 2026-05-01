from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# ---------- Interaction Schemas ----------

class InteractionCreate(BaseModel):
    """Schema for the structured form POST."""
    doctor_name: str
    hospital: Optional[str] = None
    specialty: Optional[str] = None
    interaction_type: Optional[str] = None
    product_discussed: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    notes: Optional[str] = None
    follow_up: Optional[str] = None
    outcome: Optional[str] = None


class InteractionUpdate(BaseModel):
    """Schema for editing an interaction."""
    doctor_name: Optional[str] = None
    hospital: Optional[str] = None
    specialty: Optional[str] = None
    interaction_type: Optional[str] = None
    product_discussed: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    notes: Optional[str] = None
    follow_up: Optional[str] = None
    outcome: Optional[str] = None


class InteractionOut(InteractionCreate):
    """Schema for responses — includes DB-generated fields."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- Chat Schema ----------

class ChatRequest(BaseModel):
    message: str


class SuggestRequest(BaseModel):
    context: str