from typing import Dict, Any, List
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class ReviewComment(BaseModel):
    line_reference: str = Field(description="Where the issue is roughly.")
    comment: str = Field(description="The stylisitic or architectural critique.")

class CodeReviewOutput(BaseModel):
    overall_score: int = Field(description="Score out of 10 for code style and idiomatic approach.")
    comments: List[ReviewComment] = Field(description="List of nitpicks and review comments.")
    refactored_snippet: str = Field(description="A beautifully styled Pythonic refactor.")

class CodeReviewAgent(BaseAgent):
    \"\"\"
    Strict Code Reviewer. Focuses on PEP8, variable naming, and idiomatic Python.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are a 'Staff Engineer' reviewing a Pull Request.
    The user provides working code. Do not look for logic bugs.
    Look for STYLE bugs: poor naming, unidiomatic loops, missing type hints, overly nested logic.
    Be strict. Provide a score out of 10, specific line-by-line nitpicks, and a clean refactored version.
    Output exclusively as JSON.
    \"\"\"

    def run(self, code: str) -> Dict[str, Any]:
        self.logger.info("Executing Strict Code Review phase...")

        prompt = f"Code for Pull Request Review:\\n{code}"
        
        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=CodeReviewOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"Review Agent failed: {e}")
            return {"error": str(e)}
