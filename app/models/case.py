from sqlalchemy import Column, String, Boolean, Float, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class CaseModel(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fir_id = Column(String(50), unique=True, index=True, nullable=False)
    complainant_name = Column(String(100), nullable=False)
    offense_summary = Column(Text, nullable=False)
    is_violent = Column(Boolean, default=False)
    
    # Eligibility Output
    offense_identified = Column(String(150), nullable=True)
    is_violent_crime = Column(Boolean, default=False)
    max_punishment_years = Column(Integer, default=0)
    eligible_for_ai = Column(Boolean, default=False)
    recommended_tier = Column(String(50), nullable=True)
    eligibility_reasoning = Column(Text, nullable=True)

    # Readiness and Meter
    readiness_score = Column(Float, default=0.0)
    is_ready_for_decision = Column(Boolean, default=False)
    prosecution_weight = Column(Float, default=50.0)
    defense_weight = Column(Float, default=50.0)
    missing_elements = Column(JSON, default=list)

    # Opt-In Choice State
    opt_in_prompt_required = Column(Boolean, default=False)
    user_chosen_mode = Column(String(20), default="PENDING")  # PENDING, AI_JUDGE, HUMAN_JUDGE

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())