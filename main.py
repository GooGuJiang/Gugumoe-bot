import json
import os
import os.path
import random
import sys
import time
import traceback
import zipfile
from typing import Union

import requests
import telebot
import yaml
from loguru import logger
from telebot import types
from nslookup import Nslookup
import shlex
import glob


import jrrp
from generator import genImage

if os.path.exists("./config.yml") is False:  # 初始化Bot
    logger.info(f"开始第一次初始化")
    logger.info(f"创建 config.yml 配置文件")
    with open("./config.yml", 'wb') as f:
        f.write(bytes(
            "botToken: \nosuToken: \nproxybool: False\nproxy: {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'}\napikey: \nmusicapi: \nmusicphone: \nmusicpwd: ",
            'utf-8'))
        f.close()
    logger.info(f"创建文件夹")
    dir_list = ["./img", "./tmp", "./user", "./user/jrrp", "./user/shoutmp", "./user/osu", "./output"]
    for d in dir_list:
        if not os.path.exists(d):
            logger.info("正在创建 " + d)
            os.makedirs(d, exist_ok=True)
        else:
            logger.info("已存在 " + d)
    logger.info(f"文件夹创建完毕")
    logger.info(f"开始下载表情包文件")
    r = requests.get("https://gmoe.cc/bot/img.zip")
    with open("./tmp/img.zip", 'wb') as code:
        code.write(r.content)
    code.close()
    logger.info(f"表情包下载完成")
    logger.info(f"开始解压文件")
    zip_file = zipfile.ZipFile("./tmp/img.zip")
    zip_list = zip_file.namelist()
    for f in zip_list:
        logger.info(f"解压 {f}")
        zip_file.extract(f, "./")
    zip_file.close()
    logger.info(f"文件解压完毕")
    logger.info(f"清除缓存")
    os.remove("./tmp/img.zip")
    logger.info(f"初始化完毕请填写配置文件然后重新运行本程序!")
    sys.exit()
else:
    logger.info(f"加载配置文件")
    with open('config.yml', 'r') as f:  # 读取配置文件?
        bot_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    none_list = []
    for k in bot_config:
        if bot_config[k] is None:
            none_list.append(k)
    if len(none_list) != 0:
        logger.error(f"配置文件 {','.join(none_list)} 未填写")
        sys.exit()

    else:
        bot = telebot.TeleBot(bot_config["botToken"], parse_mode="markdown")
        import osu

        if bot_config["proxybool"]:
            from telebot import apihelper

            apihelper.proxy = bot_config['proxy']
        logger.info(f"配置文件加载完毕!")
# 初始化结束
# 函数

import jrrp
import hhsh
import guip
import make_img


def get_zl_text(textlt,colon_bool=False) -> Union[str, bool]:  # 指令提取
    try:
        textcomm = textlt
        if ' ' in textlt:
            char_1 = ' '
            commkgkg = textcomm.find(char_1)
            outip = textcomm[commkgkg + 1:len(textcomm)]
            if outip is None:
                return False
            else:
                if colon_bool:
                    return outip.replace('"', "").replace("'", "")
                else:
                    return outip
        else:
            return False
    except:
        return False


# 命令
@bot.message_handler(commands=['jrrp'])
def send_jrrp(message):
    # print(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.username != "Channel_Bot":
        get_jrrp = jrrp.jrrp_get(message.from_user.id)
        bot.reply_to(message, "你今天的人品是: *{0}*\n{1}".format(get_jrrp, jrrp.jrrp_text(get_jrrp)))
    else:
        get_jrrp = jrrp.jrrp_get(message.sender_chat.id)
        bot.reply_to(message, "你今天的人品是: *{0}*\n{1}".format(get_jrrp, jrrp.jrrp_text(get_jrrp)))


@bot.message_handler(commands=['gu'])
def send_gu(message):
    try:
        path_file_name_wjj=os.listdir("./img/") #获取当前文件夹下个数
        path_file_name=glob.glob(pathname=f'./img/{path_file_name_wjj[random.randint(0,len(path_file_name_wjj)-1)]}/*.webp') #获取当前文件夹下个数
        sti = open(path_file_name[random.randint(0,len(path_file_name)-1)], 'rb')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
        sti.close()
    except Exception:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '呜呜呜....图片没上传及时.......')
        traceback.print_exc()


@bot.message_handler(commands=['guhhsh'])
def send_nbnhhsh(message):
    try:
        text_rl = get_zl_text(message.text)
        if text_rl:
            bot.send_chat_action(message.chat.id, 'typing')
            hhsh_text_go = bot.reply_to(message, '正在查询请稍后...')
            text = hhsh.nbnhhsh(text_rl)
            bot.edit_message_text(text, hhsh_text_go.chat.id, hhsh_text_go.message_id)
            # bot.reply_to(message,zhihu_text)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, "你的指令出错了惹!\n(缺少参数/guhhsh [查询拼音首字母缩写释义的文本])")
    except:
        pass


@bot.message_handler(commands=['moetrace'])
def gudlsoundcloud(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        msg_json = json.loads(json.dumps(message.json))
        try:
            file_info = bot.get_file(msg_json['reply_to_message']['photo'][-1]['file_id'])
        except:
            bot.reply_to(message, "呜呜呜...请使用 /moetrace 回复一张图片 ")
            return None
        botjson = bot.reply_to(message, "咕小酱正在获取图片请稍后....")

        # file = requests.get(
        #    'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))

        if bot_config['proxybool']:
            bot_proxies = bot_config['proxy']
        else:
            bot_proxies = None

        get_info_about = requests.get("https://api.trace.moe/me", proxies=bot_proxies).json()

        bot.edit_message_text("咕小酱正在努力搜索中...", botjson.chat.id, botjson.message_id)

        file = requests.get(
            'https://api.telegram.org/file/bot{0}/{1}'.format(bot_config["botToken"], file_info.file_path),
            proxies=bot_proxies)

        # get_info = requests.get("https://api.trace.moe/search?cutBorders&anilistInfo&url={}".format(urllib.parse.quote_plus(url)),proxies=bot_proxies).json()

        get_info = requests.post("https://api.trace.moe/search?cutBorders&anilistInfo",
                                 files={"image": file.content},
                                 proxies=bot_proxies).json()

        get_title_jp = get_info["result"][0]["anilist"]["title"]["native"]
        get_title_en = get_info["result"][0]["anilist"]["title"]["english"]

        get_title = "「" + str(get_title_jp) + "」(" + str(get_title_en) + ")"

        get_similarity = round(get_info["result"][0]["similarity"] * 100, 2)

        get_video = get_info["result"][0]["video"]

        quota = get_info_about["quota"]
        quotaUsed = get_info_about["quotaUsed"]
        quota_text = str(quota - (quotaUsed + 1))

        if get_similarity >= 85:
            bot.edit_message_text("搜索信息如下↓ \n图片来自番剧: \n *" + str(get_title) + "* \n相似度: *" + str(
                get_similarity) + "* %\n查询额度还有: *" + str(quota_text) + "* 次", botjson.chat.id,
                                  botjson.message_id)
            bot.send_video_note(botjson.chat.id, get_video, reply_to_message_id=botjson.message_id)
        else:
            bot.edit_message_text("搜索信息如下↓ \n图片来自番剧: \n *" + str(get_title) + "* \n相似度: *" + str(
                get_similarity) + "* %\n查询额度还有: *" + str(
                quota_text) + "* 次\n预览视频因为 *相似度* 小于等于 *85%* 不予展示", botjson.chat.id,
                                  botjson.message_id)


    except Exception as err:
        bot.send_chat_action(message.chat.id, 'typing')
        # bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(err),chat_json_img.chat.id, chat_json_img.message_id)
        chat_json_img = bot.reply_to(message, '呜呜呜...咕小酱遇到了严重问题......\n错误日志: ' + str(err))
        time.sleep(3)
        bot.delete_message(chat_json_img.chat.id, chat_json_img.message_id)


@bot.message_handler(commands=['httpcat'])
def httpcat(message):
    if not get_zl_text(message.text):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, "呜呜呜...指令有问题\n(指令格式 */httpcat [Http代码]*)")
    else:
        try:
            if bot_config['proxybool']:
                bot_proxies = bot_config['proxy']
            else:
                bot_proxies = None
            text_rl = get_zl_text(message.text)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            try:
                chat_json_img = bot.send_photo(message.chat.id, "https://http.cat/" + str(text_rl),
                                               reply_to_message_id=message.message_id)
            except:
                chat_json_img = bot.send_photo(message.chat.id, "https://http.cat/404",
                                               reply_to_message_id=message.message_id)
        except Exception:
            # traceback.print_exc()
            bot.send_chat_action(message.chat.id, 'typing')
            # bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(bot_err),chat_json_img.chat.id, chat_json_img.message_id)
            # chat_json_img = bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(bot_err))
            chat_json_img = bot.reply_to(message,
                                         '呜呜呜...咕小酱遇到了严重问题......\n错误日志: ' + traceback.format_exc())
            time.sleep(3)
            bot.delete_message(chat_json_img.chat.id, chat_json_img.message_id)


@bot.message_handler(commands=['guosu_std_mini'])
def osu_std_mini(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_std_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chat_json_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "std", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                else:
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                    bot.send_chat_action(message.chat.id, 'typing')
                    chat_json_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_std_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chat_json_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "std", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                else:
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                    bot.send_chat_action(message.chat.id, 'typing')
                    chat_json_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chat_json_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "std", True, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
            else:
                bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                chat_json_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chat_json_out.chat.id,
                                  chat_json_out.message_id)
            time.sleep(10)
            bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)


@bot.message_handler(commands=['guosu_taiko_mini'])
def osu_taiko_mini(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_taiko_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chat_json_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "taiko", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                else:
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                    chat_json_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_taiko_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chat_json_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "taiko", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                else:
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                    chat_json_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chat_json_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "taiko", True, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
            else:
                bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
                chat_json_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chat_json_out.chat.id,
                                  chat_json_out.message_id)
            time.sleep(10)
            bot.delete_message(chat_json_out.chat.id, chat_json_out.message_id)


@bot.message_handler(commands=['guosu_catch_mini'])
def osu_catch_mini(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "catch", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "catch", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "catch", True, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_mania_mini'])
def osu_mania_mini(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_mania_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "mania", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_mania_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "mania", True, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "mania", True, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_std'])
def osu_std(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_std [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "std", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_std [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "std", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "std", False, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_taiko'])
def osu_taiko(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_taiko [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "taiko", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_taiko [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "taiko", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "taiko", False, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_catch'])
def osu_catch(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "catch", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "catch", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "catch", False, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_mania'])
def osu_mania(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_mania [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "mania", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_mania [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                osu_img_bool = osu.get_osu_img(get_osu_id, "mania", False, message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/' + osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/' + osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool = osu.get_osu_img(get_json["user_id"], "mania", False, message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/' + osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti, reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/' + osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message, "查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_bind'])
def osu_bind(message):
    if message.from_user.username != "Channel_Bot":
        get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
        if get_osu_id is not False:
            get_osu_name = osu.get_osuid(get_osu_id)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,
                         "您已经绑定了 *" + str(get_osu_name["username"]) + "* \n 如需解绑请使用 */guosu_unbind* 指令")
            return None
    else:
        get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
        if get_osu_id is not False:
            get_osu_name = osu.get_osuid(get_osu_id)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,
                         "您已经绑定了 *" + str(get_osu_name["username"]) + "* \n 如需解绑请使用 */guosu_unbind* 指令")
            return None

    if not get_zl_text(message.text):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, "呜呜呜...指令有问题\n(指令格式 */guosu_bind [ID/用户名]* 来绑定)")
    else:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is not False:
                get_osu_name = osu.get_osuid(get_osu_id)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "您已经绑定了 *" + str(
                    get_osu_name["username"]) + "* \n 如需解绑请使用 */guosu_unbind* 指令")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_bind = bot.reply_to(message, "正在绑定...")
                try:
                    get_osu_id = osu.get_osuid(get_zl_text(message.text))
                    if osu.sql_osu2tg_id(get_osu_id["user_id"]) is False:
                        osu.sql_wq(message.from_user.id, get_osu_id["user_id"])
                        bot.edit_message_text("*绑定成功!*", chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                    else:
                        bot.edit_message_text("抱歉,该 OSU ID 已经绑定其他 Telegram ID,如需绑定请联系机器人管理员!",
                                              chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                except Exception:
                    bot.edit_message_text("*绑定失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",
                                          chatjson_bind.chat.id, chatjson_bind.message_id)
                    time.sleep(10)
                    bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is not False:
                get_osu_name = osu.get_osuid(get_osu_id)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "您已经绑定了 *" + str(
                    get_osu_name["username"]) + "* \n 如需解绑请使用 */guosu_unbind* 指令")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_bind = bot.reply_to(message, "正在绑定...")
                try:
                    get_osu_id = osu.get_osuid(get_zl_text(message.text))
                    if osu.sql_osu2tg_id(get_osu_id["user_id"]) is False:
                        osu.sql_wq(message.sender_chat.id, get_osu_id["user_id"])
                        bot.edit_message_text("*绑定成功!*", chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                    else:
                        bot.edit_message_text("抱歉,该 OSU ID 已经绑定其他 Telegram ID,如需绑定请联系机器人管理员!",
                                              chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                except Exception:
                    bot.edit_message_text("*绑定失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",
                                          chatjson_bind.chat.id, chatjson_bind.message_id)
                    time.sleep(10)
                    bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)


@bot.message_handler(commands=['guosu_unbind'])
def osu_unbind(message):
    get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
    if get_osu_id is False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, "您未绑定 OSU ID \n 如需绑定请使用 */guosu_bind [ID/用户名]* 指令")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_bind = bot.reply_to(message, "正在解除绑定...")

        if osu.sql_del(message.from_user.id) is False:
            osu.sql_wq(message.from_user.id, get_osu_id["user_id"])
            bot.edit_message_text("*解绑失败*,请联系机器人管理员!", chatjson_bind.chat.id, chatjson_bind.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
        else:
            bot.edit_message_text("*解绑成功!*", chatjson_bind.chat.id, chatjson_bind.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)


@bot.message_handler(commands=['guosu_played'])
def osu_played(message):
    if not get_zl_text(message.text):
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_played [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                try:
                    get_osu_new_info = osu.get_osu_new_played(get_osu_id)
                    get_osu_map_json = osu.get_osu_beatmaps(get_osu_new_info["beatmap_id"])
                except:
                    bot.edit_message_text("*查询失败*,没有查询到您的最近游玩记录!", chatjson_out.chat.id,
                                          chatjson_out.message_id)
                    return None

                try:
                    get_pp = str(get_osu_new_info["pp"])
                except:
                    get_pp = "暂不可用"

                out_text = f"*最新游玩成绩*\n *{get_osu_map_json['title_unicode']} - {get_osu_map_json['artist_unicode']}*\n获得PP: *{get_pp}*\n评级: *{get_osu_new_info['rank']}*\n分数: *{get_osu_new_info['score']}*\n最大连击数: *{get_osu_new_info['maxcombo']}*"
                out_text += f"\n300G: *{get_osu_new_info['countgeki']}*\n300: *{get_osu_new_info['count300']}*\n100K: *{get_osu_new_info['countkatu']}*\n100: *{get_osu_new_info['count100']}*\n50: *{get_osu_new_info['count50']}*\nMiss: *{get_osu_new_info['countmiss']}*\n"
                out_text += f"游玩时间: *{osu.time_cn(get_osu_new_info['date'])}*"
                bot.edit_message_text(out_text, chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, "呜呜呜...指令有问题\n(缺少参数 */guosu_mania [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
                try:
                    get_osu_new_info = osu.get_osu_new_played(get_osu_id)
                    get_osu_map_json = osu.get_osu_beatmaps(get_osu_new_info["beatmap_id"])
                except:
                    bot.edit_message_text("*查询失败*,没有查询到您的最近游玩记录!", chatjson_out.chat.id,
                                          chatjson_out.message_id)
                    return None
                try:
                    get_pp = str(get_osu_new_info["pp"])
                except:
                    get_pp = "暂不可用"

                out_text = f"*最新游玩成绩*\n{get_osu_map_json['title_unicode']} - {get_osu_map_json['artist_unicode']}\n获得PP: *{get_pp}*\n评级: *{get_osu_new_info['rank']}*\n分数: *{get_osu_new_info['score']}*\n最大连击数: *{get_osu_new_info['maxcombo']}*"
                out_text += f"\n300G: *{get_osu_new_info['countgeki']}*\n300: *{get_osu_new_info['count300']}*\n100K: *{get_osu_new_info['countkatu']}*\n100: *{get_osu_new_info['count100']}*\n50: *{get_osu_new_info['count50']}*\nMiss: *{get_osu_new_info['countmiss']}*\n"
                out_text += f"游玩时间: *{osu.time_cn(get_osu_new_info['date'])}*"
                bot.edit_message_text(out_text, chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message, "正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            try:
                get_osu_new_info = osu.get_osu_new_played(get_json["user_id"])
                get_osu_map_json = osu.get_osu_beatmaps(get_osu_new_info["beatmap_id"])
            except:
                bot.edit_message_text("*查询失败*,没有查询到此玩家的最近游玩记录!", chatjson_out.chat.id,
                                      chatjson_out.message_id)
                return None

            try:
                get_pp = str(get_osu_new_info["pp"])
            except:
                get_pp = "暂不可用"

            out_text = f"*最新游玩成绩*\n{get_osu_map_json['title_unicode']} - {get_osu_map_json['artist_unicode']}\n获得PP: *{get_pp}*\n评级: *{get_osu_new_info['rank']}*\n分数: *{get_osu_new_info['score']}*\n最大连击数: *{get_osu_new_info['maxcombo']}*"
            out_text += f"\n300G: *{get_osu_new_info['countgeki']}*\n300: *{get_osu_new_info['count300']}*\n100K: *{get_osu_new_info['countkatu']}*\n100: *{get_osu_new_info['count100']}*\n50: *{get_osu_new_info['count50']}*\nMiss: *{get_osu_new_info['countmiss']}*\n"
            out_text += f"游玩时间: *{osu.time_cn(get_osu_new_info['date'])}*"
            bot.edit_message_text(out_text, chatjson_out.chat.id, chatjson_out.message_id)


        except Exception:
            traceback.print_exc()
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!", chatjson_out.chat.id,
                                  chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)


@bot.message_handler(commands=['guosu_help'])
def osu_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, """
咕小酱OSU功能如下
*/guosu_std_mini 查询OSU模式-迷你卡片*
*/guosu_taiko_mini 查询太鼓模式-迷你卡片*
*/guosu_catch_mini 查询接水果模式-迷你卡片*
*/guosu_mania_mini 查询下落模式-迷你卡片*
*/guosu_std 查询OSU模式*
*/guosu_taiko 查询太鼓模式*
*/guosu_catch 查询接水果模式*
*/guosu_mania 查询下落模式*
*/guosu_played 查询最新游玩成绩(测试)*
*/guosu_bind 绑定 OSU ID*
*/guosu_unbind 解除绑定 OSU ID*
*/guosu_help 查看本帮助*
""")



@bot.message_handler(commands=['guip_ping'])
def guip_ping(message):
    input_ip = get_zl_text(message.text)
    if input_ip is False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, "呜呜呜...指令有问题\n(指令格式 */guip_ping [ip]*)")
        return None

    get_lo = guip.is_localhost_ip(input_ip)

    if get_lo is True:
        bot.reply_to(message, "呜呜呜...咕小酱发现此 *地址* 为 *本地主机* 地址,无法检测")
        return None

    bot.send_chat_action(message.chat.id, 'typing')
    chatjson_ip = bot.reply_to(message, "正在进行 Ping ...")
    get_gu = guip.gu_ping(input_ip)
    if get_gu is False:
        bot.edit_message_text("呜呜呜...咕小酱无法Ping通此 *地址* 或者 这个地址就根本 *不存在* !", chatjson_ip.chat.id,
                              chatjson_ip.message_id)
        return None

    bot.edit_message_text(f"Ping 信息如下:\n```\n{get_gu}\n```", chatjson_ip.chat.id, chatjson_ip.message_id)


@bot.message_handler(commands=['gu_eat'])
def gu_eat(message):
    # print(message)
    bot.send_chat_action(message.chat.id, 'typing')
    jsonjx = json.loads(json.dumps(message.json))

    try:
        jsonjx['reply_to_message']
    except:
        bot.reply_to(message, "呜呜呜...请使用 */gu_eat* 回复一个人的消息 ")
        return None

    del_json = bot.reply_to(message, '正在生成图片...')
    try:
        if jsonjx['reply_to_message']["from"]["id"] != 136817688:
            user_id = jsonjx['reply_to_message']["from"]["id"]
            out_img_info = bot.get_user_profile_photos(user_id)
            out_img_info = out_img_info.photos[0][-1]
            img_url = bot.get_file_url(out_img_info.file_id)
        else:
            user_id = jsonjx['reply_to_message']["sender_chat"]["id"]
            out_img_file_id = bot.get_chat(user_id)
            img_url = bot.get_file_url(out_img_file_id.photo.big_file_id)

    except Exception:
        bot.reply_to(message, "呜呜呜...咕小酱获取不到此人的头像 ")
        bot.delete_message(del_json.chat.id, del_json.message_id)
        return None

    if bot_config['proxybool']:
        bot_proxies = bot_config['proxy']
    else:
        bot_proxies = None

    # get_info_about = requests.get("https://api.trace.moe/me", proxies=bot_proxies).json()

    req = requests.get(img_url, stream=True, proxies=bot_proxies)
    out_file_name = f"gu_eat_{user_id}.png"
    if req.status_code == 200:
        open(f'./tmp/{out_file_name}', 'wb').write(req.content)

    out_rl = make_img.make_eat_img(f'{out_file_name}', str(user_id))

    try:
        sti = open(out_rl, 'rb')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
        bot.delete_message(del_json.chat.id, del_json.message_id)
        sti.close()
        os.remove(out_rl)
        os.remove(f'./tmp/{out_file_name}')
    except Exception:
        bot.delete_message(del_json.chat.id, del_json.message_id)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '呜呜呜....图片没上传及时.......')
        traceback.print_exc()


@bot.message_handler(commands=['gu_5000choyen'])
def gu_5000choyen(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        get_text = get_zl_text(message.text)
        if not get_text:
            bot.reply_to(message, "呜呜呜...请使用 */gu_5000choyen* (上半句)|(下半句) 来生成图片 ")
            return None
        keyword = get_text
        del_json = bot.reply_to(message, "咕小酱正在努力生成请稍后...")
        if '｜' in keyword:

            keyword = keyword.replace('｜', '|')
        elif '|' in keyword:
            pass
        else:
            bot.reply_to(message, "未检测到分句 格式 (上半句)|(下半句)")
            return None
        if message.from_user.username != "Channel_Bot":
            file_id = message.from_user.id
        else:
            file_id = message.sender_chat.id
        upper = keyword.split("|")[0]
        downer = keyword.split("|")[1]
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        img = genImage(word_a=upper, word_b=downer)
        img.save(f"./tmp/temp{file_id}.png")
        sti = open(f"./tmp/temp{file_id}.png", 'rb')
        bot.send_sticker(message.chat.id, sti, reply_to_message_id=message.message_id)
        bot.delete_message(del_json.chat.id, del_json.message_id)
        sti.close()
        os.remove(f"./tmp/temp{file_id}.png")
    except:
        bot.reply_to(message, "呜呜呜...生成图片错误了惹,请尝试重新生成...")


@bot.message_handler(commands=['guip_trace'])
def gu_test(message):
    if message.from_user.username == "Channel_Bot":
        bot.edit_message_text("该功能不支持频道马甲使用...",sc_text_go.chat.id, sc_text_go.message_id)
        return None
    else:
        user_id = message.from_user.id

    get_text = get_zl_text(message.text,True)
    if get_text is False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, "呜呜呜...指令有问题\n(指令格式 */guip_trace [ip]*)")
        return None

    markup = types.InlineKeyboardMarkup()
    get_text = shlex.quote(get_text)
    sc_text_go=bot.reply_to(message,"请稍等...")

    if guip.yes_or_no_ip(get_text) == True:
        import subprocess
        bot.edit_message_text(f"正在路由追踪(V4) *{get_text}* 请稍后...",sc_text_go.chat.id,sc_text_go.message_id)
        p=subprocess.Popen(f"nexttrace {get_text}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        tmp_text = ""
        while p.poll() is None:
            line=p.stdout.readline().decode("utf8")
            line=line.replace('\n', '')
            tmp_text += line + "\n"
            #print(line)

        for i in range(50):#去除多余空行
            tmp_text= tmp_text.strip("\n")
        
        bot.edit_message_text(f"正在生成图片请稍后...",sc_text_go.chat.id,sc_text_go.message_id)
        text_list_tmp = tmp_text.split("\n")
        make_img_bool = guip.make_ip_img(text_list_tmp,user_id)
        if make_img_bool == True:
            bot.edit_message_text(f"正在上传图片请稍后...",sc_text_go.chat.id,sc_text_go.message_id)
            bot.send_photo(sc_text_go.chat.id, open(f'./tmp/{user_id}-ip.jpg', 'rb'),reply_to_message_id=sc_text_go.message_id)
            os.remove(f'./tmp/{user_id}-ip.jpg')
            bot.edit_message_text(f"已完成路由跟踪",sc_text_go.chat.id,sc_text_go.message_id)
        else:
            bot.edit_message_text(f"生成图片失败,请稍后再试",sc_text_go.chat.id,sc_text_go.message_id)
        return None

    if guip.yes_or_no_ip6(get_text) == True:
        import subprocess
        bot.edit_message_text(f"正在路由追踪(V6) *{get_text}* 请稍后...",sc_text_go.chat.id,sc_text_go.message_id)
        p=subprocess.Popen(f"nexttrace {get_text}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        tmp_text = ""
        while p.poll() is None:
            line=p.stdout.readline().decode("utf8")
            line=line.replace('\n', '')
            tmp_text += line + "\n"
            #print(line)

        for i in range(50):#去除多余空行
            tmp_text= tmp_text.strip("\n")
        
        bot.edit_message_text(f"正在生成图片请稍后...",sc_text_go.chat.id,sc_text_go.message_id)
        text_list_tmp = tmp_text.split("\n")
        make_img_bool = guip.make_ip_img(text_list_tmp,user_id)
        if make_img_bool == True:
            bot.edit_message_text(f"正在上传图片请稍后...",sc_text_go.chat.id,sc_text_go.message_id)
            bot.send_photo(sc_text_go.chat.id, open(f'./tmp/{user_id}-ip.jpg', 'rb'),reply_to_message_id=sc_text_go.message_id)
            os.remove(f'./tmp/{user_id}-ip.jpg')
            bot.edit_message_text(f"已完成路由跟踪",sc_text_go.chat.id,sc_text_go.message_id)
        else:
            bot.edit_message_text(f"生成图片失败,请稍后再试",sc_text_go.chat.id,sc_text_go.message_id)
        return None

    do_list = ["4","6","q"]
    name_list = ["V4","V6","取消"]
    
    for i in range(0,3):
        mkjson = '{"ip":"'+str(get_text)+'","u":"'+str(user_id)+'","do":"'+str(do_list[i])+'"}'
        btn = types.InlineKeyboardButton(name_list[i], callback_data=str(mkjson))
        markup.add(btn)
        #print(len(mkjson.encode('utf-8')),mkjson)
    if len(mkjson.encode('utf-8')) > 64:
        bot.edit_message_text(f"抱歉域名长度不能超过 *29* 个字符,如果超过请使用IP地址",sc_text_go.chat.id, sc_text_go.message_id)
        return None
    bot.edit_message_text("请选择需要测试网际协议版本:",sc_text_go.chat.id, sc_text_go.message_id,reply_markup=markup)

# -----------------------------------------

# DNS库预加载
dns_query = Nslookup()
dns_query = Nslookup(dns_servers=["8.8.8.8","223.5.5.5"], verbose=False, tcp=False)


# -----------------------------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_handle(call):
    out_json = json.loads(str(call.data))
    #print(out_json)
    if str(call.from_user.id) != out_json["u"]:
        bot.answer_callback_query(call.id, "抱歉你不是指令发起人,无法操作")
        return None

    bot.answer_callback_query(call.id, "正在通知咕小酱...")
    
    if out_json["do"] == "q":#识别
        bot.edit_message_text("已取消测试",call.json["message"]["chat"]["id"],call.message.id)
        return None
        #bot.delete_message(out_json["cd"], out_json["ud"])

    if out_json["do"] == "4":#识别
        #if guip.yes_or_no_ip(out_json["ip"]) == True:
        ips_record = dns_query.dns_lookup(out_json["ip"])
        if len(ips_record.answer) > 1:
            markup = types.InlineKeyboardMarkup()
            for i in range(0,len(ips_record.answer)):
                mkjson = '{"ip":"'+str(ips_record.answer[i])+'","u":"'+str(out_json["u"])+'","do":"4"}'
                btn = types.InlineKeyboardButton(str(ips_record.answer[i]), callback_data=str(mkjson))
                markup.add(btn)
            mkjson = '{"ip":"'+str(ips_record.answer[i])+'","u":"'+str(out_json["u"])+'","do":"q"}'
            btn = types.InlineKeyboardButton("取消", callback_data=str(mkjson))
            markup.add(btn)
            bot.edit_message_text("检测到该域名有多个IP地址,请选择一个进行测试:",call.json["message"]["chat"]["id"],call.message.id,reply_markup=markup)
        else:
            import subprocess
            #print(out_json["ip"])
            if guip.yes_or_no_ip(out_json["ip"]) == False:
                ips_record = dns_query.dns_lookup(out_json["ip"])
                if len(ips_record.answer) == 0:
                    bot.edit_message_text("无法解析该地址,请检查域名或地址是否正确",call.json["message"]["chat"]["id"],call.message.id)
                    return None
                bot.edit_message_text(f"正在路由追踪(V4) *{ips_record.answer[0]}* 请稍后...",call.json["message"]["chat"]["id"],call.message.id)
                p=subprocess.Popen(f"nexttrace {ips_record.answer[0]}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            else:
                bot.edit_message_text(f"正在路由追踪(V4) *{out_json['ip']}* 请稍后...",call.json["message"]["chat"]["id"],call.message.id)
                p=subprocess.Popen(f"nexttrace {out_json['ip']}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            tmp_text = ""
            while p.poll() is None:
                line=p.stdout.readline().decode("utf8")
                line=line.replace('\n', '')
                tmp_text += line + "\n"
                #print(line)

            for i in range(50):#去除多余空行
                tmp_text= tmp_text.strip("\n")
            
            bot.edit_message_text(f"正在生成图片请稍后...",call.json["message"]["chat"]["id"],call.message.id)
            text_list_tmp = tmp_text.split("\n")
            make_img_bool = guip.make_ip_img(text_list_tmp,call.from_user.id)
            if make_img_bool == True:
                bot.edit_message_text(f"正在上传图片请稍后...",call.json["message"]["chat"]["id"],call.message.id)
                bot.send_photo(call.json["message"]["chat"]["id"], open(f'./tmp/{call.from_user.id}-ip.jpg', 'rb'),reply_to_message_id=call.message.id)
                os.remove(f'./tmp/{call.from_user.id}-ip.jpg')
                bot.edit_message_text(f"已完成路由跟踪",call.json["message"]["chat"]["id"],call.message.id)
            else:
                bot.edit_message_text(f"生成图片失败,请稍后再试",call.json["message"]["chat"]["id"],call.message.id)

    if out_json["do"] == "6":#识别
        #if guip.yes_or_no_ip(out_json["ip"]) == True:
        ips_record = dns_query.dns_lookup6(out_json["ip"])
        if len(ips_record.answer) > 1:
            markup = types.InlineKeyboardMarkup()
            for i in range(0,len(ips_record.answer)):
                mkjson = '{"ip":"'+str(ips_record.answer[i])+'","u":"'+str(out_json["u"])+'","do":"6"}'
                btn = types.InlineKeyboardButton(str(ips_record.answer[i]), callback_data=str(mkjson))
                markup.add(btn)
            mkjson = '{"ip":"'+str(ips_record.answer[i])+'","u":"'+str(out_json["u"])+'","do":"q"}'
            btn = types.InlineKeyboardButton("取消", callback_data=str(mkjson))
            markup.add(btn)
            bot.edit_message_text("检测到该域名有多个IP地址,请选择一个进行测试:",call.json["message"]["chat"]["id"],call.message.id,reply_markup=markup)
        else:
            import subprocess
            #print(out_json["ip"])
            if guip.yes_or_no_ip6(out_json["ip"]) == False:
                ips_record = dns_query.dns_lookup6(out_json["ip"])
                if len(ips_record.answer) == 0:
                    bot.edit_message_text("无法解析该地址,请检查域名或地址是否正确",call.json["message"]["chat"]["id"],call.message.id)
                    return None
                bot.edit_message_text(f"正在路由追踪(V6) *{ips_record.answer[0]}* 请稍后...",call.json["message"]["chat"]["id"],call.message.id)
                p=subprocess.Popen(f"nexttrace {ips_record.answer[0]}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            else:
                bot.edit_message_text(f"正在路由追踪(V6) *{out_json['ip']}* 请稍后...",call.json["message"]["chat"]["id"],call.message.id)
                p=subprocess.Popen(f"nexttrace {out_json['ip']}", shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            tmp_text = ""
            while p.poll() is None:
                line=p.stdout.readline().decode("utf8")
                line=line.replace('\n', '')
                tmp_text += line + "\n"
                #print(line)

            for i in range(50):#去除多余空行
                tmp_text= tmp_text.strip("\n")
            
            bot.edit_message_text(f"正在生成图片请稍后...",call.json["message"]["chat"]["id"],call.message.id)
            text_list_tmp = tmp_text.split("\n")
            make_img_bool = guip.make_ip_img(text_list_tmp,call.from_user.id)
            if make_img_bool == True:
                bot.edit_message_text(f"正在上传图片请稍后...",call.json["message"]["chat"]["id"],call.message.id)
                bot.send_photo(call.json["message"]["chat"]["id"], open(f'./tmp/{call.from_user.id}-ip.jpg', 'rb'),reply_to_message_id=call.message.id)
                os.remove(f'./tmp/{call.from_user.id}-ip.jpg')
                bot.edit_message_text(f"已完成路由跟踪",call.json["message"]["chat"]["id"],call.message.id)
            else:
                bot.edit_message_text(f"生成图片失败,请稍后再试",call.json["message"]["chat"]["id"],call.message.id)

@bot.inline_handler(lambda query: query.query == 'jrrp')
def query_jrrpt(inline_query):
    try:
        # print("jrrp=",inline_query)
        localtime = time.localtime(time.time())
        markup = types.InlineKeyboardMarkup()
        get_jrrp = jrrp.jrrp_get(inline_query.from_user.id)
        btn1 = types.InlineKeyboardButton("我也试试", switch_inline_query="jrrp")
        markup.add(btn1)
        r = types.InlineQueryResultArticle('1',
                                           f'今日人品 {localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}',
                                           types.InputTextMessageContent(
                                               "你今天的人品是: {0}\n{1}".format(
                                                   get_jrrp,
                                                   jrrp.jrrp_text_init(get_jrrp)
                                               )
                                           ),
                                           thumb_url="https://s3.bmp.ovh/imgs/2022/07/02/e15481817c097493.jpg",
                                           description="测测你今天的人品!", reply_markup=markup)
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception:
        traceback.print_exc()



@bot.inline_handler(lambda query: True)
def query_mr(inline_query):
    try:
        # print(inline_query)
        localtime = time.localtime(time.time())
        markup = types.InlineKeyboardMarkup()
        get_jrrp = jrrp.jrrp_get(inline_query.from_user.id)
        btn1 = types.InlineKeyboardButton("我也试试", switch_inline_query="jrrp")
        markup.add(btn1)
        r = types.InlineQueryResultArticle('5', f'今日人品 {localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}',
                                           types.InputTextMessageContent(
                                               "你今天的人品是: {0}\n{1}".format(
                                                   get_jrrp,
                                                   jrrp.jrrp_text_init(get_jrrp)
                                               )
                                           ),
                                           thumb_url="https://s3.bmp.ovh/imgs/2022/07/02/e15481817c097493.jpg",
                                           description="测测你今天的人品!", reply_markup=markup)
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception:
        traceback.print_exc()


# Main
if __name__ == '__main__':
    while True:
        try:
            # logger = telebot.logger
            # telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
            logger.info(f"启动成功!")
            bot.polling()


        except Exception:
            logger.error(f"遇到错误正在重启:")
            traceback.print_exc()
        time.sleep(1)
