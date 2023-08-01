import asyncio
import datetime
from gugumoe_bot.settings import settings
from gugumoe_bot.db.mongodb_helper import MongoDBHelper


async def test_mongodb_helper():
    # 创建一个 MongoDBHelper 对象
    mongodb_helper = MongoDBHelper()

    # 初始化数据库
    await mongodb_helper.initialize_db()

    # 测试用户ID和日期
    user_id = "test_user"
    date = datetime.date.today()

    # 检查用户是否存在
    user_exists = await mongodb_helper.check_user_exists(user_id)
    print(f"User exists before insertion: {user_exists}")

    # 插入新的人品数值
    luck_number = 88
    await mongodb_helper.store_daily_luck(user_id, date, luck_number)

    # 再次检查用户是否存在
    user_exists = await mongodb_helper.check_user_exists(user_id)
    print(f"User exists after insertion: {user_exists}")

    # 获取插入的人品数值
    luck_info = await mongodb_helper.get_daily_luck(user_id, date)
    print(f"Retrieved luck info: {luck_info}")

    # 更新人品数值
    new_luck_number = 99
    await mongodb_helper.update_daily_luck(user_id, date, new_luck_number=new_luck_number)

    # 获取更新后的人品数值
    updated_luck_info = await mongodb_helper.get_daily_luck(user_id, date)
    print(f"Updated luck info: {updated_luck_info}")


# 运行测试
loop = asyncio.get_event_loop()
loop.run_until_complete(test_mongodb_helper())
loop.close()
