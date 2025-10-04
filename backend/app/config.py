import os
from typing import Dict, Any

class Settings:
    """Application settings configuration"""
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "AI Resume Optimizer"
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {'.pdf', '.docx'}
    UPLOAD_DIR: str = "uploads"
    
    # NLP Settings
    SPACY_MODEL: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # ATS Scoring Weights
    ATS_WEIGHTS: Dict[str, float] = {
        "skills_match": 0.35,
        "keywords": 0.25,
        "formatting": 0.15,
        "readability": 0.15,
        "grammar": 0.10
    }
    
    def __init__(self):
        # Create upload directory if it doesn't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

settings = Settings()
