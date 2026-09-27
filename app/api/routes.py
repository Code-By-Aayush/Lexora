from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.intake import CaseIntakeRequest, CompleteCaseAnalysisResponse
from app.services.eligibility_engine import CaseEligibilityEngine
from app.services.readiness_engine import ReadinessAndMeterEngine
from app.core.database import get_db
from app.models.case import CaseModel
from pydantic import BaseModel

router = APIRouter()
eligibility_engine = CaseEligibilityEngine()

class OptInChoiceRequest(BaseModel):
    fir_id: str
    chosen_mode: str  # "AI_JUDGE" or "HUMAN_JUDGE"

@router.post("/process-case", response_model=CompleteCaseAnalysisResponse)
async def process_case(case: CaseIntakeRequest, db: Session = Depends(get_db)):
    try:
        # 1. Run Core AI & Algorithmic Engines
        eligibility = eligibility_engine.evaluate_case(case)
        readiness_and_meter = ReadinessAndMeterEngine.calculate_metrics(case)
        opt_in_required = eligibility.eligible_for_ai

        # 2. Persist or Update Record in PostgreSQL
        existing_case = db.query(CaseModel).filter(CaseModel.fir_id == case.fir_id).first()
        
        if not existing_case:
            db_case = CaseModel(
                fir_id=case.fir_id,
                complainant_name=case.complainant_name,
                offense_summary=case.offense_summary,
                is_violent=case.is_violent,
                offense_identified=eligibility.offense_identified,
                is_violent_crime=eligibility.is_violent_crime,
                max_punishment_years=eligibility.max_punishment_years,
                eligible_for_ai=eligibility.eligible_for_ai,
                recommended_tier=eligibility.recommended_tier,
                eligibility_reasoning=eligibility.reasoning,
                readiness_score=readiness_and_meter.readiness_score,
                is_ready_for_decision=readiness_and_meter.is_ready_for_decision,
                prosecution_weight=readiness_and_meter.prosecution_weight,
                defense_weight=readiness_and_meter.defense_weight,
                missing_elements=readiness_and_meter.missing_elements,
                opt_in_prompt_required=opt_in_required
            )
            db.add(db_case)
            db.commit()
            db.refresh(db_case)

        return CompleteCaseAnalysisResponse(
            fir_id=case.fir_id,
            eligibility=eligibility,
            readiness_and_meter=readiness_and_meter,
            opt_in_prompt_required=opt_in_required
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/select-opt-in")
async def select_opt_in(request: OptInChoiceRequest, db: Session = Depends(get_db)):
    case = db.query(CaseModel).filter(CaseModel.fir_id == request.fir_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case FIR not found")
    
    if request.chosen_mode not in ["AI_JUDGE", "HUMAN_JUDGE"]:
        raise HTTPException(status_code=400, detail="Invalid choice. Must be AI_JUDGE or HUMAN_JUDGE.")
    
    case.user_chosen_mode = request.chosen_mode
    db.commit()
    
    return {
        "fir_id": request.fir_id,
        "status": "Updated",
        "user_chosen_mode": request.chosen_mode,
        "message": f"Case routing set to {request.chosen_mode} successfully."
    }