from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Secure Code Quality Evaluator"
    VERSION: str = "1.0.0"
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Evaluation Settings
    MAX_CODE_LENGTH: int = 100000  # Maximum code length in characters
    DEFAULT_EVALUATORS: list = ["correctness", "maintainability", "security"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
