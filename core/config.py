import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    \"\"\"
    Application Settings
    Managed by Pydantic to ensure type safety and proper validation.
    \"\"\"
    PROJECT_NAME: str = "CodeMentor AI"
    VERSION: str = "1.0.0"
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Application Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # MCP Server configuration
    MCP_HOST: str = os.getenv("MCP_HOST", "127.0.0.1")
    MCP_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    # Security Configuration
    MAX_INPUT_LENGTH: int = int(os.getenv("MAX_INPUT_LENGTH", "4000"))
    ENABLE_SANDBOX: bool = os.getenv("ENABLE_SANDBOX", "true").lower() == "true"
    
    # Agent configurations
    DEFAULT_MODEL: str = "gemini-2.5-pro" # Fast and smart model for complex logic

settings = Settings()

if not settings.GEMINI_API_KEY:
    # Important warning for deployment
    print("WARNING: GEMINI_API_KEY is not set in environment variables.")
