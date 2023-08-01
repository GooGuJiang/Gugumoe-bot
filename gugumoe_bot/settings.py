from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """
    Bot settings.
    """

    log_level: str = "INFO"

    # Bot token
    token: str = ""
    proxy: str | int = None
    username: str = ""

    # MongoDB settings
    mongodb_host: str = "192.168.31.181"
    mongodb_port: int = 27017
    mongodb_user_name: str = ""
    mongodb_password: str = ""
    mongodb_db_name: str = "gugumoe_bot"
    mongodb_collection_jrrp: str = "jrrp"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="GUGUMOE_BOT_",
        env_file_encoding="utf-8",
    )


settings = Settings()
