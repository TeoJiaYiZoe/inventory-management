from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Inventory API"
    ENVIRONMENT: str = "local"
    DYNAMODB_TABLE: str = "Inventory"
    AWS_REGION: str = "ap-southeast-1"
    API_KEY: Optional[str] = None
    CORS_ORIGINS: str = "*"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()