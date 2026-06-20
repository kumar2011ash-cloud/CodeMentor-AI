from typing import Dict, Any
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class QAOutput(BaseModel):
    final_explanation: str = Field(description="Polished, highly encouraging, and clear final explanation.")
    final_code: str = Field(description="The finalized, verified, and styled code.")
    signoff: str = Field(description="A short supportive signoff.")

class QAAgent(BaseAgent):
    \"\"\"
    The Final Gatekeeper. Ensures the pipeline output is formatted perfectly for the user.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are the final Quality Assurance and Presentation specialist.
    You will receive a raw solution pipeline output.
    Your job is to construct a flawless, beautifully written final response.
    Ensure the code is perfect. Ensure the tone is mentoring, supportive, and extremely clear.
    Output exclusively as JSON.
    \"\"\"

    def run(self, raw_data: str) -> Dict[str, Any]:
        self.logger.info("Executing final QA pipeline gate...")

        prompt = f"Raw Pipeline Data to Polish:\\n{raw_data}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=QAOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"QA Agent failed: {e}")
            return {"error": str(e)}
