from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class CompanyOutput(BaseModel):
    cultural_fit_advice: str = Field(description="How this company expects code to be written (e.g. Google C++ styles vs Meta rapid iteration).")
    expected_follow_ups: str = Field(description="System design or scaling questions this specific company usually asks.")
    refactored_for_company: str = Field(description="Code refactored to match company specific patterns.")

class CompanyAgent(BaseAgent):
    \"\"\"
    Company-Specific Coding Agent.
    Tailors the review or solution specifically to a target company's engineering culture.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are an expert on Tech Company coding cultures (Google, Meta, Amazon, Apple, Netflix, etc.).
    Given a company name and a piece of code, explain how that specific company would grade the code, what scaling follow-ups they would ask, and refactor the code to match their internal style guides.
    Output exclusively as JSON.
    \"\"\"

    def run(self, company_name: str, code: str) -> Dict[str, Any]:
        self.logger.info(f"Executing Company-Specific Review for {company_name}...")

        prompt = f"Target Company: {company_name}\\n\\nCode to Review:\\n{code}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=CompanyOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Company Agent failed: {e}")
            return {"error": str(e)}
