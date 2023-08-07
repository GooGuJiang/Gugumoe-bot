import sys
from pathlib import Path
from tempfile import gettempdir

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """
    Bot settings.
    """

    log_level: str = "INFO"

    # Add Field for required fields
    token: str = Field(None, description="Bot token")
    proxy: str = ""
    username: str = Field(None, description="Username")
    mongodb_url: str = Field(None, description="MongoDB URL")
    mongodb_db_name: str = "gugumoe_bot"
    mongodb_collection_jrrp: str = "jrrp"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="GUGUMOE_BOT_",
        env_file_encoding="utf-8",
    )

    def __post_init__(self):
        # List of required attributes
        required_attributes = ['token', 'username', 'mongodb_url']

        for attribute in required_attributes:
            if getattr(self, attribute) in ("", None):
                logger.error(f"Missing required attribute: {attribute}")
                sys.exit(1)


settings = Settings()
