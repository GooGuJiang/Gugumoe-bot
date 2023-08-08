import pickle

import redis.asyncio as redis

from gugumoe_bot.settings import settings

redis_setting = {
    "host": settings.redis_host,
    "port": settings.redis_port,
    "password": settings.redis_password,
}


class RedisHelper:

    def __init__(self):
        self.redis = redis.Redis(host=redis_setting["host"], port=redis_setting["port"],
                                 password=redis_setting["password"])

    async def set_object(self, key, obj, expire=None):
        """将对象存储到Redis中。"""
        serialized_value = pickle.dumps(obj)
        await self.redis.set(key, serialized_value)

        if expire:
            await self.redis.expire(key, expire)

    async def get_object(self, key):
        """从Redis中检索对象。"""
        serialized_value = await self.redis.get(key)
        if serialized_value:
            return pickle.loads(serialized_value)
        else:
            return None

    async def delete_object(self, key):
        """从Redis中删除对象。"""
        await self.redis.delete(key)
        return True


# 使用示例
if __name__ == '__main__':
    import asyncio


    async def main():
        redis_helper = RedisHelper()
        await redis_helper.set_object("test_key", {"name": "John", "age": 30}, expire=60)
        retrieved_data = await redis_helper.get_object("test_key")
        print(retrieved_data)


    asyncio.run(main())
