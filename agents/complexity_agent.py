from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class ComplexityOutput(BaseModel):
    time_complexity_big_o: str = Field(description="Exact Time Complexity, e.g., O(N log N).")
    space_complexity_big_o: str = Field(description="Exact Space Complexity, e.g., O(N).")
    bottlenecks: str = Field(description="Explanation of the slowest parts of the code.")
    optimization_advice: str = Field(description="Actionable advice on how to improve the complexity.")

class ComplexityAgent(BaseAgent):
    \"\"\"
    Acts as a Performance Engineering Specialist.
    Analyzes code to determine precise Big O notation for time/space, and identifies bottlenecks.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are an expert Performance Engineer and Algorithm Analyst.
    Given a piece of code and potentially its problem statement, your task is to strictly determine the Time Complexity and Space Complexity using Big O notation.
    Identify any performance bottlenecks and suggest how they could be improved.
    Output your analysis as JSON.
    \"\"\"

    def run(self, problem_statement: str, code: str) -> Dict[str, Any]:
        self.logger.info("Analyzing algorithmic complexity...")

        prompt = f"Problem Statement:\\n{problem_statement}\\n\\n"
        prompt += f"Code to Analyze:\\n{code}\\n\\n"
        prompt += "Output the Big O analysis, bottlenecks, and optimization advice."

        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=ComplexityOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Complexity Agent failed: {e}")
            return {"error": str(e)}
