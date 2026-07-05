from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma2:latest"
    upload_dir: str = "temp_uploads"
    cache_ttl: int = 3600

    model_config = {"env_prefix": "PHYSICS_"}

settings = Settings()
