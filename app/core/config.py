import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

    # basic validation
    def validate(self):
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set. Put it in your .env")

settings = Settings()
settings.validate()
