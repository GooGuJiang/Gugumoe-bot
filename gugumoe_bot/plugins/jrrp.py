import asyncio
import concurrent.futures
import socket
from datetime import datetime

import httpx
import ntplib
import pytz
from loguru import logger

from gugumoe_bot.db.mongodb_helper import MongoDBHelper
from gugumoe_bot.plugin_interface import PluginInterface

mongo = MongoDBHelper()


async def jrrp_text_init(nub_in):
    nub = int(nub_in)
    if nub == 100:
        return "100 人品好评!!!"
    elif nub >= 90:
        return "今天的人品非常不错呢"
    elif nub >= 70:
        return "哇,人品还挺好的!"
    elif nub >= 60:
        return "今天是 非常¿ 不错的一天呢!"
    elif nub > 50:
        return f"{nub} 你的人品还不错呢"
    elif nub == 50:
        return "五五开！"
    elif nub >= 40:
        return f"还好还好只有 {nub}"
    elif nub >= 20:
        return f"{nub} 这数字太....要命了"
    elif nub >= 0:
        return "抽大奖¿"


def get_local_time_in_utc_plus_8():
    local_time = datetime.now()
    local_time = pytz.timezone('UTC').localize(local_time)
    local_time_in_utc_plus_8 = local_time.astimezone(pytz.timezone('Asia/Shanghai'))
    return local_time_in_utc_plus_8


async def get_random_number():
    url = 'https://www.random.org/integers/?num=1&min=0&max=100&col=1&base=10&format=plain&rnd=new'
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
    return int(res.text.strip("\n"))


def get_ntp_time_sync(host="pool.ntp.org"):
    ntp_client = ntplib.NTPClient()
    try:
        response = ntp_client.request(host)
        return datetime.fromtimestamp(response.tx_time)
    except (ntplib.NTPException, socket.gaierror, socket.timeout):
        logger.error("Error while syncing with NTP server, using local time in UTC+8 instead")
        return get_local_time_in_utc_plus_8()


async def get_ntp_time(host="time.apple.com"):
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        time = await loop.run_in_executor(pool, get_ntp_time_sync, host)
        return time


async def convert_to_tz(time: datetime, tz: str = "Asia/Shanghai"):
    return time.astimezone(pytz.timezone(tz))


async def get_jrrp(user_id: int) -> str:
    """Get jrrp from database."""
    try:
        try:
            today = await get_ntp_time()
            today = await convert_to_tz(today)
            today = today.date()
        except Exception as e:
            logger.error(f"Error while getting NTP time: {e}, using local time instead")
            today = datetime.now()
            today = today.date()

        user_id = str(user_id)
        document = await mongo.get_daily_luck(user_id)
        # 只取日期, 不取时间
        if document is not None and document["date"].date() == today:
            return f'<b>今天的人品是：</b>{document["jrrp_nub"]}\n你今天已经抽过人品了哦'
        else:
            try:
                luck_number = await get_random_number()
            except Exception as e:
                luck_number = hash(str(user_id) + str(today)) % 100
            # 如果日期不是今天，就存入数据库
            if document is not None and document["date"].date() != today:
                await mongo.update_daily_luck(user_id, today, luck_number)
            else:
                await mongo.store_daily_luck(user_id, today, luck_number)
            return f'<b>今天的人品是：</b>{luck_number}\n{await jrrp_text_init(luck_number)}'
    except Exception as e:
        logger.error(f"Error while getting jrrp: {e}")
        return "获取人品失败了呢"


class JrrpPlugin(PluginInterface):
    command = 'jrrp'

    async def handle_command(self, bot, message):
        """Handle the /jrrp command."""
        if message.from_user.id == 136817688:
            user_id = message.sender_chat.id
        else:
            user_id = message.from_user.id
        await bot.send_chat_action(message.chat.id, 'typing')
        await bot.reply_to(message, await get_jrrp(user_id), parse_mode='HTML')
