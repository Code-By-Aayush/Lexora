import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models.case import CaseModel

Base.metadata.create_all(bind=engine)

SYNTHETIC_CASES = [
    {
        "fir_id": "FIR-2026-MH-0101",
        "complainant_name": "Anil Sharma",
        "offense_summary": "Traffic violation: Jumped red light at Virar intersection, recorded by CCTV.",
        "is_violent": False,
        "offense_identified": "Motor Vehicles Act - Signal Jumping",
        "eligible_for_ai": True,
        "recommended_tier": "Stage 1 (AI Resolution)",
        "readiness_score": 95.0,
        "is_ready_for_decision": True,
        "prosecution_weight": 80.0,
        "defense_weight": 20.0
    },
    {
        "fir_id": "FIR-2026-MH-0102",
        "complainant_name": "Sita Verma",
        "offense_summary": "Civil Property Dispute: Dispute regarding boundary wall encroachment without violence.",
        "is_violent": False,
        "offense_identified": "Property Encroachment / Civil Dispute",
        "eligible_for_ai": True,
        "recommended_tier": "Stage 2 (Step-by-Step)",
        "readiness_score": 65.0,
        "is_ready_for_decision": False,
        "prosecution_weight": 55.0,
        "defense_weight": 45.0,
        "missing_elements": ["Land Survey Report Missing"]
    },
    {
        "fir_id": "FIR-2026-MH-0103",
        "complainant_name": "State of Maharashtra",
        "offense_summary": "Armed Robbery and Physical Assault at commercial establishment.",
        "is_violent": True,
        "offense_identified": "BNS - Robbery and Bodily Harm",
        "eligible_for_ai": False,
        "recommended_tier": "Stage 3 (Human Court)",
        "readiness_score": 85.0,
        "is_ready_for_decision": True,
        "prosecution_weight": 50.0,
        "defense_weight": 50.0
    }
]

def seed():
    db = SessionLocal()
    try:
        for cdata in SYNTHETIC_CASES:
            existing = db.query(CaseModel).filter(CaseModel.fir_id == cdata["fir_id"]).first()
            if not existing:
                case = CaseModel(**cdata)
                db.add(case)
        db.commit()
        print("Successfully seeded synthetic database records!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()