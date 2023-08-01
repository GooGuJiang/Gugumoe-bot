# 插件：echo.py
from gugumoe_bot.plugin_interface import PluginInterface


class EchoPlugin(PluginInterface):
    command = 'guecho'

    async def handle_command(self, bot, message):
        text = message.text.split(' ', 1)[1]
        await bot.reply_to(message, text)
