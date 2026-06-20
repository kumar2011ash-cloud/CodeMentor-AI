from typing import Dict, Any, List
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class BugReport(BaseModel):
    issue_type: str = Field(description="E.g., Logical Error, Syntax Error, OutOfBounds.")
    description: str = Field(description="Detailed explanation of the bug.")
    fix_suggestion: str = Field(description="How to fix this specific bug.")

class DebugOutput(BaseModel):
    bug_list: List[BugReport] = Field(description="List of identified bugs.")
    corrected_code: str = Field(description="Fully corrected production-ready code.")
    explanation: str = Field(description="Overall explanation of what went wrong and how it was resolved.")

class DebugAgent(BaseAgent):
    \"\"\"
    Acts as a Senior Code Reviewer.
    Analyzes user-provided incorrect code, finds hidden bugs, and provides detailed fixes.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are an elite Code Debugger and Senior Security Reviewer.
    The user will provide you with a problem statement and an incorrect code implementation.
    Your job is to thoroughly analyze the provided code, find ALL logical, syntax, and hidden edge-case bugs.
    Return a structured list of bugs, the fully corrected code, and an overarching explanation.
    \"\"\"

    def run(self, problem_statement: str, incorrect_code: str, error_message: str = "") -> Dict[str, Any]:
        self.logger.info("Analyzing incorrect code for bugs...")

        prompt = f"Problem Statement:\\n{problem_statement}\\n\\n"
        prompt += f"Incorrect Code:\\n{incorrect_code}\\n\\n"
        if error_message:
            prompt += f"Observed Error Output:\\n{error_message}\\n\\n"
            
        prompt += "Identify the bugs, provide an explanation, and output the corrected code as JSON."

        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=DebugOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Debug Agent failed: {e}")
            return {"error": str(e)}
