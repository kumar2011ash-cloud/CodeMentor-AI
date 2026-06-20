from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class ExplanationOutput(BaseModel):
    summary: str = Field(description="A high-level sentence summarizing the logic.")
    step_by_step_breakdown: str = Field(description="A detailed walkthrough of how the code works.")
    analogy: str = Field(description="A real-world analogy explaining the algorithm.")

class ExplanationAgent(BaseAgent):
    \"\"\"
    Acts as a Patient Teacher.
    Explains complex code blocks and algorithms tailored to the user's expertise level.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are an award-winning Computer Science Professor.
    Your goal is to explain code and algorithms clearly.
    You adapt your explanation based on the requested 'mode' (Beginner, Intermediate, Expert).
    Provide a step-by-step breakdown and a helpful real-world analogy.
    Output as JSON.
    \"\"\"

    def run(self, code: str, mode: str = "Beginner") -> Dict[str, Any]:
        self.logger.info(f"Generating explanation in {mode} mode...")

        prompt = f"Explanation Target Mode: {mode}\\n\\n"
        prompt += f"Code to Explain:\\n{code}\\n\\n"
        prompt += "Provide the summary, breakdown, and an analogy."

        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=ExplanationOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Explanation Agent failed: {e}")
            return {"error": str(e)}
