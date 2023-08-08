import hashlib

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import gugumoe_bot.utils.nslookup_helper as nslookup_helper
from gugumoe_bot.plugin_interface import PluginInterface
from gugumoe_bot.utils.nexttrace_helper import NextTraceHelper
from gugumoe_bot.utils.redis_helper import RedisHelper

CANCEL_SEC = 60


def generate_hash(data: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()


class NexttracePlugin(PluginInterface):
    command = 'gutrace'

    def __init__(self):
        self.nexttrace_helper = NextTraceHelper()
        self.redis_helper = RedisHelper()

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

        if get_identify_and_extract_ip[0] == "Domain":
            host = get_identify_and_extract_ip[1]
            msg_tmp = await bot.reply_to(message, "咕小酱正在尝试解析域名，请稍等哦。")
            get_records = nslookup_helper.get_records(host)
            if len(get_records['A']) == 0 and len(get_records['AAAA']) == 0:
                bot.edit_message_text("抱歉，咕小酱貌似无法解析这个域名呢。", message.chat.id, msg_tmp.message_id)
                return
            if len(get_records['A']) == 1 and len(get_records['AAAA']) == 0:
                ipv4 = get_records['A'][0]
                bot.edit_message_text("咕小酱已经成功解析域名，正在尝试进行下路由追踪，请稍等哦。", message.chat.id,
                                      msg_tmp.message_id)
                # TODO: Add nexttrace
            if len(get_records['A']) == 0 and len(get_records['AAAA']) == 1:
                ipv6 = get_records['AAAA'][0]
                bot.edit_message_text("咕小酱已经成功解析域名，正在尝试进行路由追踪，请稍等哦。", message.chat.id,
                                      msg_tmp.message_id)
                # TODO: Add nexttrace
            if len(get_records['A']) >= 1 and len(get_records['AAAA']) >= 1:
                make_json_v4 = {
                    "action": "nexttrace",
                    "ipv4": get_records['A'],
                    "message_id": msg_tmp.message_id,
                    "chat_id": message.chat.id,
                    "host": host
                }
                make_json_v6 = {
                    "action": "nexttrace",
                    "ipv6": get_records['AAAA'],
                    "message_id": msg_tmp.message_id,
                    "chat_id": message.chat.id,
                    "host": host
                }
                cancel_json = {
                    "action": "cancel",
                    "message_id": msg_tmp.message_id,
                    "chat_id": message.chat.id
                }
                make_hash_v4 = generate_hash(str(make_json_v4))
                make_hash_v6 = generate_hash(str(make_json_v6))
                cancel_hash = generate_hash(str(cancel_json))
                await self.redis_helper.set_object(make_hash_v4, make_json_v4, expire=CANCEL_SEC)
                await self.redis_helper.set_object(make_hash_v6, make_json_v6, expire=CANCEL_SEC)
                await self.redis_helper.set_object(cancel_hash, cancel_json, expire=CANCEL_SEC)
                keyboard = InlineKeyboardMarkup()
                keyboard.add(
                    InlineKeyboardButton("IPv4", callback_data=make_hash_v4),
                    InlineKeyboardButton("IPv6", callback_data=make_hash_v6)
                )
                keyboard.add(InlineKeyboardButton("取消", callback_data=cancel_hash))
                await bot.edit_message_text(
                    f"咕小酱检测到这个域名同时存在IPv4和IPv6地址，请在 {CANCEL_SEC} 秒内选择要检测的类型：",
                    message.chat.id,
                    msg_tmp.message_id, reply_markup=keyboard)
                return

    async def handle_callback_query(self, bot, call):
        await bot.answer_callback_query(call.id, "正在通知咕小酱响应事件，请稍等哦。")
