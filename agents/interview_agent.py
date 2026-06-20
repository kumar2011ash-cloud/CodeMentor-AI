from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class InterviewOutput(BaseModel):
    feedback: str = Field(description="Critique of the user's current direction.")
    probing_question: str = Field(description="A Socratic question to guide the user without giving the answer.")
    red_flags: str = Field(description="Any major interview red flags noticed (e.g. ignoring edge cases).")

class InterviewAgent(BaseAgent):
    \"\"\"
    Mock FAANG Interviewer. Does NOT give the code away. Uses Socratic method.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are a Staff Software Engineer at FAANG conducting a technical interview.
    The user gives you a problem and their current code/thoughts.
    DO NOT write the final code for them.
    Instead, evaluate their direction, ask a probing follow-up question to test their understanding, and note any red flags.
    Output exclusively as JSON.
    \"\"\"

    def run(self, problem_statement: str, user_code: str) -> Dict[str, Any]:
        self.logger.info("Executing Mock Interview phase...")

        prompt = f"The Problem:\\n{problem_statement}\\n\\nUser's Current Progress:\\n{user_code}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=InterviewOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Interview Agent failed: {e}")
            return {"error": str(e)}
