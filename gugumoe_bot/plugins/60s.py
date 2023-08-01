import re
import httpx

from gugumoe_bot.plugin_interface import PluginInterface


class SixtyReadTheWorld(PluginInterface):
    command = "60s"

    @staticmethod
    async def get_calendar() -> bytes:
        async with httpx.AsyncClient(http2=True, follow_redirects=True) as client:
            response = await client.get(
                "https://api.03c3.cn/zb"
            )
            if response.is_error:
                raise ValueError(f"60s日历获取失败，错误码：{response.status_code}")
            return response.content

    async def handle_command(self, bot, message):
        img = await self.get_calendar()
        await bot.send_photo(message.chat.id, img)