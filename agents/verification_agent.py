from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class VerificationOutput(BaseModel):
    passes_static_analysis: bool = Field(description="Are there syntax or typing issues?")
    logical_integrity: str = Field(description="Explanation of mental walk-through of the code.")
    verification_status: str = Field(description="Either 'APPROVED' or 'REJECTED'")

class VerificationAgent(BaseAgent):
    \"\"\"
    Acts as a Verification system, simulating a dry-run of the code to catch hallucinated syntax or obvious logic drifts.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are a Verification Sandbox Proxy. We do not have a real execution environment right now.
    You must mentally 'dry-run' the provided code against common edge cases.
    Check for syntax validity, import errors, or logic holes.
    If the code fails the mental dry-run, mark it REJECTED.
    Otherwise, mark it APPROVED.
    Output exclusively as JSON.
    \"\"\"

    def run(self, problem_statement: str, code: str) -> Dict[str, Any]:
        self.logger.info("Executing Verification phase...")

        prompt = f"Problem Context: {problem_statement}\\n\\nCode to Verify:\\n{code}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=VerificationOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Verification Agent failed: {e}")
            return {"error": str(e)}
