import os
from langchain_openai import ChatOpenAI
from app.schemas.intake import EligibilityResponse, CaseIntakeRequest
from app.core.config import settings

class CaseEligibilityEngine:
    def __init__(self):
        # Initialize Groq via OpenAI-compatible API endpoint
        self.llm = ChatOpenAI(
            model="openai/gpt-oss-120b",  # ✅ confirmed available in your Groq account
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            temperature=0.0
        )
        # Bind LLM to strictly output the Pydantic schema
        self.structured_llm = self.llm.with_structured_output(EligibilityResponse)

    def evaluate_case(self, case: CaseIntakeRequest) -> EligibilityResponse:
        system_prompt = (
            "You are Lexora's AI Case Eligibility Engine for the Indian Judiciary.\n"
            "Analyze the incoming FIR summary and evaluate eligibility under BNS, BNSS, and BSA.\n"
            "Rules:\n"
            "1. If the offense is violent, sexual, against minors, or involves punishment > 7 years, "
            "set eligible_for_ai = False and recommended_tier = 'Stage 3 (Human Court)'.\n"
            "2. If it is a minor, routine, compoundable, or traffic/cheque bounce matter (punishment <= 2 years), "
            "set eligible_for_ai = True and recommended_tier = 'Stage 1 (AI Resolution)'.\n"
            "3. If moderately complex civil/property dispute without violence, set eligible_for_ai = True "
            "and recommended_tier = 'Stage 2 (Step-by-Step)'.\n"
        )

        user_message = f"FIR Summary: {case.offense_summary}\nIs Violent: {case.is_violent}"

        # Execute LLM evaluation
        response = self.structured_llm.invoke([
            ("system", system_prompt),
            ("user", user_message)
        ])
        return response