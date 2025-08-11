from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    API_KEY_FINANCIAL_DATA: str = "your_api_key_here"

    class Config:
        env_file = ".env"

settings = Settings()
