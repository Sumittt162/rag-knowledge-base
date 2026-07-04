from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # This reads GROQ_API_KEY from your .env file automatically
    groq_api_key: str = Field(..., description="Your Groq API key")

    # These have sensible defaults — you don't need to set them
    llm_model: str = Field(default="llama-3.3-70b-versatile")
    chunk_size: int = Field(default=800)
    chunk_overlap: int = Field(default=150)
    retrieval_k: int = Field(default=4)
    db_path: str = Field(default="data/faiss_db")

# This line creates one shared settings object the whole app uses
settings = Settings()