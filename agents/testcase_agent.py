from typing import Dict, Any, List
from pydantic import BaseModel, Field
from agents.base_agent import BaseAgent
from core.utils import safe_json_loads

class TestCase(BaseModel):
    type: str = Field(description="E.g., normal, edge-case, hidden, stress")
    input_data: str = Field(description="The input to the function.")
    expected_output: str = Field(description="The expected correct output.")
    reason: str = Field(description="Why this test case is necessary.")

class TestCaseOutput(BaseModel):
    test_cases: List[TestCase] = Field(description="A comprehensive list of generated test cases.")
    weak_solution_detector: str = Field(description="Hints on what type of weak logic would fail these tests.")

class TestCaseAgent(BaseAgent):
    \"\"\"
    Acts as a QA/Test Automation Engineer.
    Given a problem, it generates standard, edge, and hidden test cases to ensure robust solutions.
    \"\"\"

    SYSTEM_PROMPT = \"\"\"
    You are an expert QA Engineer and Competitive Programming TestCase Designer.
    Your goal is to break weak implementations.
    Given a problem statement, produce a comprehensive list of test cases including:
    - Normal cases
    - Extreme edge cases (e.g., empty arrays, MaxInt bounds)
    - Tricky/Hidden cases that commonly trip up beginners.
    Provide the input formatting, expected output formatting, and why each test is valuable.
    \"\"\"

    def run(self, problem_statement: str) -> Dict[str, Any]:
        self.logger.info("Generating test cases for the problem...")

        prompt = f"Problem Statement:\\n{problem_statement}\\n\\n"
        prompt += "Generate robust test cases including normal, edge, stress, and hidden cases as JSON."

        try:
            response_text = self._call_llm(
                system_instruction=self.SYSTEM_PROMPT,
                prompt=prompt,
                schema=TestCaseOutput
            )
            return safe_json_loads(response_text)
        except Exception as e:
            self.logger.error(f"TestCase Agent failed: {e}")
            return {"error": str(e)}
