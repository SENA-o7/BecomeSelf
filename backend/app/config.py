from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Uygulama ayarları. Değerler önce ortam değişkenlerinden, sonra .env dosyasından okunur."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://becomeself:becomeself@localhost:5432/becomeself"


settings = Settings()
