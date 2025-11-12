from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Database settings
    DB_USER: str = "kanban_user"
    DB_PASSWORD: str = "kanban_password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "kanban_db"

    # Application settings
    APP_NAME: str = "Personal Kanban Board"
    DEBUG: bool = False

    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
