import gugumoe_bot.utils.nslookup_helper as nslookup_helper
from gugumoe_bot.plugin_interface import PluginInterface
from gugumoe_bot.utils.nexttrace_helper import NextTraceHelper

nexttrace_helper = NextTraceHelper()


class NexttracePlugin(PluginInterface):
    command = 'gutrace'

    async def handle_command(self, bot, message):
        await bot.send_chat_action(message.chat.id, 'typing')
        if len(message.text.split()) == 1:
            await bot.reply_to(message, "抱歉，指令格式似乎存在错误呢。\n正确的格式应为：*/guip_trace [地址]* ",
                               parse_mode="Markdown")
            return
        host = message.text.split()[1]
        get_identify_and_extract_ip = nslookup_helper.identify_and_extract_ip(host)
        if get_identify_and_extract_ip[0] == "Unknown":
            await bot.reply_to(message, "抱歉，咕小酱貌似无法识别这个地址的类型呢。")
            return

        if get_identify_and_extract_ip[0] == "Loopback":
            await bot.reply_to(message, "抱歉，咕小酱认为这个地址是本地回环地址，已经拒绝你的请求啦。")
            return

        if get_identify_and_extract_ip[0] == "Private":
            await bot.reply_to(message, "抱歉，咕小酱认为这个地址是私有地址，已经拒绝你的请求啦。")
            return
