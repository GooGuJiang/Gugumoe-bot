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
    proxy: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="GUGUMOE_BOT_",
        env_file_encoding="utf-8",
    )


settings = Settings()
