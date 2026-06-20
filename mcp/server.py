import asyncio
import json
import logging
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
from agents.manager_agent import ManagerAgent

manager = ManagerAgent()
mcp = FastMCP("CodeMentor-AI-V2-Server")

@mcp.tool()
def solve_problem(problem_statement: str, constraints: str = "") -> str:
    \"\"\"Solves the problem using the verified pipeline.\"\"\"
    result = manager.run("solve_pipeline", problem_statement=problem_statement, constraints=constraints)
    return json.dumps(result, indent=2)

@mcp.tool()
def review_code(code: str) -> str:
    \"\"\"Strict Code Review focusing strictly on idioms and style.\"\"\"
    result = manager.run("review", code=code)
    return json.dumps(result, indent=2)

@mcp.tool()
def interview_question_generator(problem_statement: str, user_code: str) -> str:
    \"\"\"FAANG Mock Interview: Do not give the answer, ask strategic follow-up questions.\"\"\"
    result = manager.run("interview", problem_statement=problem_statement, user_code=user_code)
    return json.dumps(result, indent=2)

@mcp.tool()
def hidden_test_detector(code: str) -> str:
    \"\"\"Discovers destructive hidden edge cases for the given code.\"\"\"
    result = manager.run("hidden_test", code=code)
    return json.dumps(result, indent=2)

@mcp.tool()
def optimize_algorithm(code: str, problem_statement: str) -> str:
    \"\"\"Evaluates Big O Time and Space Complexity to optimize.\"\"\"
    result = manager.run("complexity", problem_statement=problem_statement, code=code)
    return json.dumps(result, indent=2)

@mcp.tool()
def coding_strategy(contest_details: str) -> str:
    \"\"\"Strategic advice for competitive programming contests, identifying traps.\"\"\"
    result = manager.run("strategy", contest_details=contest_details)
    return json.dumps(result, indent=2)

def main():
    logging.info("Starting CodeMentor-AI (Top 1% Build) MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()
