from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Techly marketplace"
    database_url: str
    jwt_secret: str = "SECRETKEY"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
