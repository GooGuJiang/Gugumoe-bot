from gugumoe_bot.plugin_interface import PluginInterface
from gugumoe_bot.utils.nexttrace_helper import NextTraceHelper

nexttrace_helper = NextTraceHelper()


class NexttracePlugin(PluginInterface):
    command = 'gutrace'

    async def handle_command(self, bot, message):
        bot.send_chat_action(message.chat.id, 'typing')
        if len(message.text.split()) == 1:
            await bot.reply_to(message, "请提供一个域名或者IP地址")
            return
        host = message.text.split()[1]
        print(host)
