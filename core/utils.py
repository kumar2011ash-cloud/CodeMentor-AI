import logging
import json
from typing import Any

# Configure standard logging to integrate with Streamlit and console outputs seamlessly.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)

def get_logger(name: str) -> logging.Logger:
    \"\"\"
    Returns a consistent logger across the multi-agent system.
    \"\"\"
    return logging.getLogger(name)

def safe_json_loads(data: str) -> dict:
    \"\"\"
    Safely load JSON strings into dicts, handy for agent outputs.
    Trims markdown ticks like ```json ... ``` often produced by LLMs.
    \"\"\"
    data = data.strip()
    if data.startswith("```json"):
        data = data[7:]
    if data.startswith("```"):
        data = data[3:]
    if data.endswith("```"):
        data = data[:-3]
        
    try:
        return json.loads(data.strip())
    except json.JSONDecodeError as e:
        logger = get_logger("json_util")
        logger.error(f"Failed to decode JSON: {e}")
        return {}

def format_code_block(code: str, language: str = "python") -> str:
    \"\"\"
    Formats generated code into markdown code blocks.
    \"\"\"
    return f"```{language}\\n{code}\\n```"
