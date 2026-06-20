import os
from abc import ABC, abstractmethod
from typing import Any, Dict
from google import genai
from google.genai import types

from core.config import settings
from core.utils import get_logger

class BaseAgent(ABC):
    \"\"\"
    Abstract base class for all CodeMentor AI agents.
    Provides standard Gemini client initialization, logging, and execution interface.
    \"\"\"
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        
        if not settings.GEMINI_API_KEY:
             self.logger.warning("GEMINI_API_KEY not found. Agent execution may fail.")
             # Allows instantiation (for testing/structure) but warns if key is missing.
             self.client = None
        else:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
        self.model_name = settings.DEFAULT_MODEL

    def _call_llm(self, system_instruction: str, prompt: str, schema: Any = None) -> Any:
        \"\"\"
        Utility wrapper around the Google GenAI SDK.
        Supports Structured Output if a pydantic schema is provided.
        \"\"\"
        if not self.client:
            raise ValueError("Google GenAI client is not initialized (missing API key).")
            
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2, # Keep hallucination low for coding tasks
            )
            
            if schema:
                config.response_mime_type = "application/json"
                config.response_schema = schema

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            return response.text
        except Exception as e:
            self.logger.error(f"LLM Call failed: {e}")
            raise e

    @abstractmethod
    def run(self, *args, **kwargs) -> Dict[str, Any]:
        \"\"\"
        The entrypoint for every specialized agent.
        Must return a structured dictionary or object based on specific implementation.
        \"\"\"
        pass
