from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    firebase_credentials_path: str = "firebase-credentials.json"
    firebase_web_api_key: str = ""
    steam_api_key: str = ""

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
