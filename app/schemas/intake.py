from pydantic import BaseModel, Field
from typing import List, Optional

class CaseIntakeRequest(BaseModel):
    fir_id: str = Field(..., example="FIR-2026-MH-0012")
    complainant_name: str = Field(..., example="Ramesh Kumar")
    offense_summary: str = Field(..., example="Section 138 Cheque Bounce: Dishonored cheque of Rs. 1,50,000 due to insufficient funds.")
    is_violent: bool = Field(default=False)
    has_fir_document: bool = Field(default=True)
    has_police_report: bool = Field(default=True)
    evidence_count: int = Field(default=2)
    statements_count: int = Field(default=2)
    ocr_quality_score: float = Field(default=0.95, ge=0.0, le=1.0)

class EligibilityResponse(BaseModel):
    offense_identified: str
    is_violent_crime: bool
    max_punishment_years: int
    eligible_for_ai: bool
    recommended_tier: str  # "Stage 1 (AI Resolution)", "Stage 2 (Step-by-Step)", "Stage 3 (Human Court)"
    reasoning: str

class ReadinessAndMeterResponse(BaseModel):
    readiness_score: float = Field(..., ge=0.0, le=100.0)
    is_ready_for_decision: bool
    prosecution_weight: float = Field(..., ge=0.0, le=100.0)
    defense_weight: float = Field(..., ge=0.0, le=100.0)
    missing_elements: List[str]

class CompleteCaseAnalysisResponse(BaseModel):
    fir_id: str
    eligibility: EligibilityResponse
    readiness_and_meter: ReadinessAndMeterResponse
    opt_in_prompt_required: bool