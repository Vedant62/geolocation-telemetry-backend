from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "DB_URL"

    secret: str = "YOUR_SECRET"
    algorithm: str = "HS256"
    access_token_expire_minutes : int = 30

    kafka_server_url: str = "YOUR_KAFKA_SERVER_URL" #does not need to be list of all, just one that would respond to the Metadata API

settings = Settings()

