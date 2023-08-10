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
                await bot.edit_message_text("抱歉，咕小酱貌似无法解析这个域名呢。", message.chat.id, msg_tmp.message_id)
                return
            if len(get_records['A']) == 1 and len(get_records['AAAA']) == 0:
                ipv4 = get_records['A'][0]
                gu_tmp_msg = await bot.edit_message_text("咕小酱已经成功解析域名，正在尝试进行下路由追踪，请稍等哦。",
                                                         message.chat.id,
                                                         msg_tmp.message_id)
                image_data = self.nexttrace_helper.execute_and_generate_image(ipv4)
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                await bot.send_photo(message.chat.id, image_data, reply_to_message_id=message.message_id)
                await bot.delete_message(message.chat.id, gu_tmp_msg.message_id)
                return
            if len(get_records['A']) == 0 and len(get_records['AAAA']) == 1:
                ipv6 = get_records['AAAA'][0]
                gu_tmp_msg = bot.edit_message_text("咕小酱已经成功解析域名，正在尝试进行路由追踪，请稍等哦。",
                                                   message.chat.id,
                                                   msg_tmp.message_id)
                image_data = self.nexttrace_helper.execute_and_generate_image(ipv6)
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                await bot.send_photo(message.chat.id, image_data, reply_to_message_id=message.message_id)
                await bot.delete_message(message.chat.id, gu_tmp_msg.message_id)
                return
            if len(get_records['A']) >= 1 and len(get_records['AAAA']) >= 1:
                make_json_v4 = {
                    "action": "nexttrace",
                    "ips": get_records['A'],
                    "message_id": msg_tmp.message_id,
                    "chat_id": message.chat.id,
                    "user_id": message.from_user.id,
                    "tmp_message_id": msg_tmp.message_id,
                    "host": host
                }
                make_json_v6 = {
                    "action": "nexttrace",
                    "ips": get_records['AAAA'],
                    "message_id": msg_tmp.message_id,
                    "chat_id": message.chat.id,
                    "user_id": message.from_user.id,
                    "tmp_message_id": msg_tmp.message_id,
                    "host": host
                }
                make_hash_v4 = generate_hash(str(make_json_v4))
                make_hash_v6 = generate_hash(str(make_json_v6))

                await self.redis_helper.set_object(make_hash_v4, make_json_v4, expire=CANCEL_SEC)
                await self.redis_helper.set_object(make_hash_v6, make_json_v6, expire=CANCEL_SEC)
                cancel_json = {
                    "action": "cancel",
                    "message_id": msg_tmp.message_id,
                    "chat_id": message.chat.id,
                    "user_id": message.from_user.id,
                    "tmp_message_id": msg_tmp.message_id,
                    "delete_hash_list": [make_hash_v4, make_hash_v6]
                }
                cancel_hash = generate_hash(str(cancel_json))
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
        if get_identify_and_extract_ip[0] == "IPv4" or get_identify_and_extract_ip[0] == "IPv6":
            ip = get_identify_and_extract_ip[1]
            msg_tmp = await bot.reply_to(message, "咕小酱正在尝试进行路由追踪，请稍等哦。")
            image_data = self.nexttrace_helper.execute_and_generate_image(ip)
            await bot.send_chat_action(message.chat.id, 'upload_photo')
            await bot.send_photo(message.chat.id, image_data, reply_to_message_id=message.message_id)
            await bot.delete_message(message.chat.id, msg_tmp.message_id)
            return

    async def handle_callback_query(self, bot, call):
        # await bot.answer_callback_query(call.id, "正在通知咕小酱响应事件，请稍等哦。")
        get_data = await self.redis_helper.get_object(call.data)
        if get_data is None:
            await bot.answer_callback_query(call.id, "抱歉，此请求无法找到或已失效。", show_alert=True)
            # 删除消息
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        if get_data['user_id'] != call.from_user.id:
            await bot.answer_callback_query(call.id, "抱歉，此请求不属于你。", show_alert=True)
            return
        if get_data['action'] == "cancel":
            await bot.answer_callback_query(call.id, "正在通知咕小酱响应事件，请稍等哦。")
            delete_hash_list = get_data["delete_hash_list"]
            for i in delete_hash_list:
                await self.redis_helper.delete_object(i)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            return
        if get_data['action'] == "nexttrace":
            if len(get_data["ips"]) > 1:
                await bot.answer_callback_query(call.id, "正在通知咕小酱响应事件，请稍等哦。")
                ips_list = get_data["ips"]
                keyboard = InlineKeyboardMarkup()
                delete_hash_list = []
                for i in range(min(len(ips_list), 5)):
                    ips_data = {
                        "action": "nexttrace-start",
                        "ip": ips_list[i],
                        "message_id": get_data["message_id"],
                        "chat_id": get_data["chat_id"],
                        "user_id": get_data["user_id"],
                        "tmp_message_id": get_data["tmp_message_id"],
                        "host": get_data["host"]
                    }
                    ips_hash = generate_hash(str(ips_data))
                    await self.redis_helper.set_object(ips_hash, ips_data, expire=CANCEL_SEC)
                    keyboard.add(InlineKeyboardButton(ips_list[i], callback_data=ips_hash))
                    delete_hash_list.append(ips_hash)
                cancel_json = {
                    "action": "cancel",
                    "message_id": get_data["message_id"],
                    "chat_id": get_data["chat_id"],
                    "user_id": get_data["user_id"],
                    "tmp_message_id": get_data["tmp_message_id"],
                    "delete_hash_list": delete_hash_list
                }
                cancel_hash = generate_hash(str(cancel_json))
                await self.redis_helper.set_object(cancel_hash, cancel_json, expire=CANCEL_SEC)
                keyboard.add(InlineKeyboardButton("取消", callback_data=cancel_hash))
                await bot.edit_message_text("咕小酱解析发现该域名存在多个地址，请选择一个进行路由跟踪",
                                            call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)
                return
        if get_data['action'] == "nexttrace-start":
            await bot.answer_callback_query(call.id, "正在通知咕小酱响应事件，请稍等哦。")
            ip = get_data["ip"]
            await bot.send_chat_action(call.message.chat.id, 'typing')
            gu_tmp_msg = await bot.edit_message_text("咕小酱正在尝试进行路由追踪，请稍等哦。", call.message.chat.id,
                                                     call.message.message_id)
            image_data = self.nexttrace_helper.execute_and_generate_image(ip)
            await bot.send_chat_action(call.message.chat.id, 'upload_photo')
            await bot.send_photo(call.message.chat.id, image_data, reply_to_message_id=get_data["tmp_message_id"])
            await bot.delete_message(call.message.chat.id, gu_tmp_msg.message_id)
            return
