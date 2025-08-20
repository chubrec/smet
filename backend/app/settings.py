from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_ENV: str = "dev"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "estimate"
    DB_PASSWORD: str = "estimate"
    DB_NAME: str = "estimate"
    DATABASE_URL: str | None = None
    SECRET_KEY: str = "dev"
    ALLOWED_ORIGINS: str = "*"
    DEFAULT_CURRENCY: str = "EUR"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()  # type: ignore[call-arg]

