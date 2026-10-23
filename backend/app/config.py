from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Uygulama ayarları. Değerler önce ortam değişkenlerinden, sonra .env dosyasından okunur."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://becomeself:becomeself@localhost:5432/becomeself"
    secret_key: str = "dev-only-secret-key-change-me-in-production"
    access_token_expire_minutes: int = 60 * 24 * 7

settings = Settings()
