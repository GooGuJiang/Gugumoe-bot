import datetime
from typing import Any, Dict, Optional

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from gugumoe_bot.settings import settings

CONFIG_MONGODB = {
    "host": settings.mongodb_url,
    "db_name": settings.mongodb_db_name,
    "collection_jrrp": settings.mongodb_collection_jrrp,
}


class MongoDBHelper:
    """MongoDB Helper Class."""

    def __init__(self) -> None:
        """Initializes the MongoDBHelper instance."""
        self.client = AsyncIOMotorClient(
            CONFIG_MONGODB["host"],
        )
        self.db = self.client[CONFIG_MONGODB["db_name"]]
        self.jrrp_collection = self.db[CONFIG_MONGODB["collection_jrrp"]]

    async def initialize_db(self) -> bool:
        """Initialize the database."""
        config_collection = self.db['config']
        config = await config_collection.find_one({'name': 'jrrp'})

        if config and config.get('initialized'):
            return True

        try:
            await self.jrrp_collection.create_index(
                [("user_id", 1), ("date", 1), ("jrrp_nub", 1)], unique=True
            )
            await config_collection.insert_one({'name': 'jrrp', 'initialized': True})
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False

    # 检测jrrp数据库是否存在
    async def check_jrrp_db(self) -> bool:
        """Check if the database exists."""
        try:
            await self.jrrp_collection.find_one()
            return True
        except Exception as e:
            logger.error(f"Failed to check database: {e}")
            return False

    async def store_daily_luck(self, user_id: str, date: datetime.date, luck_number: int) -> bool:
        """Store the user's luck number for the day in the database."""
        try:
            datetime_obj = datetime.datetime(date.year, date.month, date.day)
            document = {"user_id": user_id, "date": datetime_obj, "jrrp_nub": luck_number}
            await self.jrrp_collection.insert_one(document)
            return True
        except Exception as e:
            logger.error(f"Failed to store daily luck: {e}")
            return False

    # 只通过user_id获取jrrp
    async def get_daily_luck(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get the user's luck number for the day from the database."""
        try:
            document = await self.jrrp_collection.find_one({"user_id": user_id})
            return document
        except Exception as e:
            logger.error(f"Failed to get daily luck: {e}")
            return None

    async def update_daily_luck(self, user_id: str, new_date: Optional[datetime.date] = None,
                                new_luck_number: Optional[int] = None,
                                ) -> bool:
        """Update the date or luck number for a given user ID."""
        # 基于UID更新日期和幸运数值
        try:
            # datetime_obj = datetime.datetime(date.year, date.month, date.day)
            new_datetime_obj = datetime.datetime(new_date.year, new_date.month, new_date.day)
            await self.jrrp_collection.update_one(
                {"user_id": user_id},
                {"$set": {"date": new_datetime_obj, "jrrp_nub": new_luck_number}},
            )
            return True
        except Exception as e:
            logger.error(f"Failed to update daily luck: {e}")
            return False

    async def check_user_exists(self, user_id: str) -> bool:
        """Check if a user ID exists in the database."""
        try:
            document = await self.jrrp_collection.find_one({"user_id": user_id})
            return document is not None
        except Exception as e:
            logger.error(f"Failed to check user existence: {e}")
            return False
