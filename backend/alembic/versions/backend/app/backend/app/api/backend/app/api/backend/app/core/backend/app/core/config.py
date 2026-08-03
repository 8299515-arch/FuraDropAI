from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    database_url: str = Field(..., alias="DATABASE_URL")
    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", alias="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(60, alias="JWT_EXPIRE_MINUTES")
    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://localhost:5173"], alias="CORS_ORIGINS")
    aliexpress_api_key: str | None = Field(default=None, alias="ALIEXPRESS_API_KEY")
    cj_dropshipping_api_key: str | None = Field(default=None, alias="CJ_DROPSHIPPING_API_KEY")
    spocket_api_key: str | None = Field(default=None, alias="SPOCKET_API_KEY")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

settings = Settings()
