# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # MUDANÇA AQUI: Removemos o caminho '../'
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    firebase_credentials_path: str
    steam_api_key: str

settings = Settings()