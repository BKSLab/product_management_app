from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsApp(BaseSettings):
    """Класc конфигурации секретных данных для работы product_management."""

    secret_key: SecretStr
    debug: bool
    user: SecretStr
    password: SecretStr
    host: SecretStr
    db_name: SecretStr
    port: int

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


configuration_data = SettingsApp()
