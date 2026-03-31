import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PWD>@localhost:5432/<POSTGRES_DB_NAME>",
        )
        self.secret: str = os.getenv("SECRET", "<YOUR-SECRET-HERE>")
        self.algorithm: str = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )
        self.kafka_server_url: str = os.getenv("KAFKA_SERVER_URL", "localhost:9092")


settings = Settings()

