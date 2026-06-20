from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class StrategyOutput(BaseModel):
    difficulty_estimation: str = Field(description="Estimated competitive difficulty based on details.")
    time_management_advice: str = Field(description="How to budget the clock.")
    hidden_traps: str = Field(description="What to watch out for based on contest meta.")

class StrategyAgent(BaseAgent):
    \"\"\"
    Contest Strategist. Helps users figure out IF they should solve a problem, not just HOW.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are an International Grandmaster Competitive Programmer advising a student during a contest.
    You will receive context about the problem or the contest status.
    You must output a strategic plan (difficulty estimate, time management, and meta traps).
    We want strategy, not code.
    Output exclusively as JSON.
    \"\"\"

    def run(self, contest_details: str) -> Dict[str, Any]:
        self.logger.info("Executing Contest Strategy phase...")

        prompt = f"Contest / Problem Details:\\n{contest_details}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=StrategyOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Strategy Agent failed: {e}")
            return {"error": str(e)}
