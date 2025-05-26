from pydantic_settings import BaseSettings, SettingsConfigDict
import os

env_map = {
    "test": ".env.test",
    "docker": ".env.docker",
    "local": ".env.local",
}

env_file = env_map.get(os.getenv("ENV", "local"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")

    PROJECT_NAME: str = "Auth Service"

    db_user: str = "postgres"
    db_password: str = "postgres"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "auth_db"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    redis_host: str = "localhost"
    redis_port: str = "6379"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"

    JWT_SECRET_KEY: str = "super-secret"
    JWT_REFRESH_SECRET_KEY: str = "refresh-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


settings = Settings()
