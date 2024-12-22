from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Any, Dict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Tool Platform"
    VERSION: str = "1.0.0"
    UPLOAD_DIR: Path = Path("uploads")
    
    # Tool-specific configurations
    TOOL_CONFIGS: Dict[str, Any] = {
        "pdf_tools": {
            "allowed_extensions": [".pdf"],
            "max_file_size": 10_000_000  # 10MB
        },
        "image_tools": {
            "allowed_extensions": [".jpg", ".png", ".jpeg"],
            "max_file_size": 5_000_000  # 5MB
        }
    }
    
    class Config:
        case_sensitive = True

settings = Settings()