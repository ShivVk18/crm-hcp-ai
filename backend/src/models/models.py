from sqlalchemy import Column, Integer, String, Text, DateTime, func
from src.utils.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(255), nullable=False, index=True)
    hospital = Column(String(255), nullable=True)
    specialty = Column(String(100), nullable=True)
    interaction_type = Column(String(50), nullable=True)   # e.g. Visit, Call, Email
    product_discussed = Column(String(255), nullable=True)
    date = Column(String(50), nullable=True)           # e.g. 2024-05-01
    time = Column(String(50), nullable=True)           # e.g. 14:30
    notes = Column(Text, nullable=True)
    follow_up = Column(String(500), nullable=True)
    outcome = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())