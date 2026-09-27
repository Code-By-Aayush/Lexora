from app.schemas.intake import CaseIntakeRequest, ReadinessAndMeterResponse

class ReadinessAndMeterEngine:
    @staticmethod
    def calculate_metrics(case: CaseIntakeRequest) -> ReadinessAndMeterResponse:
        missing_elements = []
        
        # 1. Decision Readiness Calculation
        c_doc = 1.0 if (case.has_fir_document and case.has_police_report) else 0.5
        if not case.has_fir_document:
            missing_elements.append("Missing FIR Document")
        if not case.has_police_report:
            missing_elements.append("Missing Police Final Investigation Report")

        c_evid = min(case.evidence_count / 3.0, 1.0)
        if case.evidence_count < 2:
            missing_elements.append("Insufficient Physical/Digital Evidence Items (Minimum 2 required)")

        c_stmt = min(case.statements_count / 2.0, 1.0)
        if case.statements_count < 2:
            missing_elements.append("Missing Opposing Party / Witness Statements")

        c_ocr = case.ocr_quality_score

        # Weighted formula: Doc(30%) + Evidence(30%) + Statements(20%) + OCR(20%)
        readiness_score = round(
            (0.30 * c_doc + 0.30 * c_evid + 0.20 * c_stmt + 0.20 * c_ocr) * 100, 2
        )
        
        is_ready = readiness_score >= 80.0

        # 2. Dynamic Guilt Meter Baseline (50/50 starting neutral)
        prosecution_weight = 50.0
        
        # Shift weight based on evidence provided
        prosecution_weight += (case.evidence_count * 10.0)
        prosecution_weight = min(max(prosecution_weight, 0.0), 100.0)
        defense_weight = 100.0 - prosecution_weight

        return ReadinessAndMeterResponse(
            readiness_score=readiness_score,
            is_ready_for_decision=is_ready,
            prosecution_weight=prosecution_weight,
            defense_weight=defense_weight,
            missing_elements=missing_elements
        )