from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import json
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class SolverOutput(BaseModel):
    explanation: str = Field(description="Step-by-step logic and intuition of the solution.")
    code: str = Field(description="Production-ready runnable Python code.")
    time_complexity: str = Field(description="Time complexity (e.g., O(N))")
    space_complexity: str = Field(description="Space complexity (e.g., O(1))")

class SolverAgent(BaseAgent):
    \"\"\"
    Acts as a Senior Software Engineer.
    Analyzes the problem statement and produces the best algorithm implementation.
    \"\"\"
    
    SYSTEM_PROMPT = \"\"\"
    You are a world-class Competitive Programmer and Senior Google Engineer.
    Your mission is to solve coding problems cleanly, optimally, and accurately.
    Provide a clear, detailed explanation of your algorithm before presenting the code.
    Ensure your code uses proper type hinting, docstrings, and error handling when applicable.
    Provide the exact Time and Space complexity.
    \"\"\"

    def run(self, problem_statement: str, constraints: Optional[str] = None) -> Dict[str, Any]:
        self.logger.info("Generating solution for the provided problem...")
        
        prompt = f"Problem Statement:\\n{problem_statement}\\n"
        if constraints:
            prompt += f"\\nConstraints:\\n{constraints}\\n"
            
        prompt += "\\nProduce the output as a valid JSON object matching the requested schema."
        
        try:
            # We enforce Structured Output using the Pydantic schema
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=SolverOutput
            )
            
            result = safe_json_loads(response_text)
            return result
        except Exception as e:
            self.logger.error(f"Solver Agent failed: {e}")
            return {"error": str(e)}
