from typing import Dict, Any, List
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class HiddenTrap(BaseModel):
    trap_name: str = Field(description="Name of the trap (e.g. Integer Overflow, Off-By-One).")
    trigger_input: str = Field(description="Specific input that triggers this.")

class HiddenTestOutput(BaseModel):
    vulnerability_score: int = Field(description="1-10 on how likely this code is to fail hidden cases.")
    discovered_traps: List[HiddenTrap] = Field(description="List of destructive test cases.")

class HiddenTestAgent(BaseAgent):
    \"\"\"
    Hidden Test Case Discovery Agent.
    Specializes in finding cases that cause Time Limit Exceeded (TLE) or Memory Limit Exceeded (MLE).
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are a malicious Competitive Programming Judge.
    Your goal is to break the user's code using extreme edge cases, overflows, or worst-case complexity inputs.
    Return the vulnerability score and the exact inputs that will break the provided algorithm.
    Output exclusively as JSON.
    \"\"\"

    def run(self, code: str) -> Dict[str, Any]:
        self.logger.info("Executing Hidden Test Discovery...")

        prompt = f"Find the worst-case inputs that will break this code:\\n{code}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=HiddenTestOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Hidden Test Agent failed: {e}")
            return {"error": str(e)}
