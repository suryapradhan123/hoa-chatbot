"""
Configuration management for HOA Chatbot
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    
    # Twilio Configuration
    twilio_account_sid: str = Field(default="", alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(default="", alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_number: str = Field(default="", alias="TWILIO_WHATSAPP_NUMBER")
    
    # Application Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    documents_path: str = Field(default="./documents", alias="DOCUMENTS_PATH")
    chroma_db_path: str = Field(default="./chroma_db", alias="CHROMA_DB_PATH")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
