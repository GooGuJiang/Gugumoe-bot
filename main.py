import telebot
from telebot import types
import zipfile
import yaml
from loguru import logger
import os.path
import os
import requests
import sys
import time
import json
import glob
import random
import traceback
from generator import genImage

if os.path.exists("./config.yml") is False: # 初始化Bot
    logger.info(f"开始第一次初始化")
    logger.info(f"创建 config.yml 配置文件")
    with open("./config.yml", 'wb') as f:
        f.write(bytes("botToken: \nosuToken: \nproxybool: False\nproxy: {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'}\napikey: \nmusicapi: \nmusicphone: \nmusicpwd: ",'utf-8'))
        f.close()
    logger.info(f"创建文件夹")
    dir_list = ["./img","./tmp","./user","./user/jrrp","./user/shoutmp","./user/osu","./output"]
    for d in dir_list:
        if not os.path.exists(d):
            logger.info("正在创建 " + d)
            os.makedirs(d, exist_ok=True)
        else:
            logger.info("已存在 " + d)
    logger.info(f"文件夹创建完毕")
    logger.info(f"开始下载表情包文件")
    r =  requests.get("https://gmoe.cc/bot/img.zip")
    with open("./tmp/img.zip",'wb') as code:
        code.write(r.content)
    code.close()
    logger.info(f"表情包下载完成")
    logger.info(f"开始解压文件")
    zip_file = zipfile.ZipFile("./tmp/img.zip")
    zip_list = zip_file.namelist() 
    for f in zip_list: 
        logger.info(f"解压 {f}")
        zip_file.extract(f,"./")
    zip_file.close() 
    logger.info(f"文件解压完毕")
    logger.info(f"清除缓存")
    os.remove("./tmp/img.zip")
    jrrp.jrrp_oneload()
    logger.info(f"初始化完毕请填写配置文件然后重新运行本程序!")
    sys.exit()
else:
    logger.info(f"加载配置文件")
    with open('config.yml', 'r') as f: #读取配置文件?
        bot_config = yaml.load(f.read(),Loader=yaml.FullLoader)
    if bot_config["botToken"] == None:
        logger.error(f"配置文件 botToken 未填写")
        sys.exit()
    elif bot_config["osuToken"] == None:
        logger.error(f"配置文件 osuToken 未填写")
        sys.exit()
    elif bot_config["apikey"] == None:
        logger.error(f"配置文件 apikey 未填写")
        sys.exit()
    elif bot_config["musicapi"] == None:
        logger.error(f"配置文件 musicapi 未填写")
        sys.exit()
    elif bot_config["musicphone"] == None:
        logger.error(f"配置文件 musicphone 未填写")
        sys.exit()
    elif bot_config["musicpwd"] == None:
        logger.error(f"配置文件 musicpwd 未填写")
        sys.exit()
    else:
        bot = telebot.TeleBot(bot_config["botToken"],parse_mode="markdown")
        import osu
        if bot_config["proxybool"] == True:
            from telebot import apihelper
            apihelper.proxy = bot_config['proxy']
        logger.info(f"配置文件加载完毕!")
#初始化结束
#函数

import jrrp
import hhsh
import guip
import make_img

def get_zl_text(textlt): #指令提取
    try:
        textcomm = textlt
        if ' ' in textlt:
            char_1=' '
            commkgkg=textcomm.find(char_1)
            outip = textcomm[commkgkg+1:len(textcomm)]
            if outip == None:
                return False
            else:
                return outip
        else:
            return False
    except:
        return False

#命令
@bot.message_handler(commands=['jrrp'])
def send_jrrp(message):
    #print(message)
    bot.send_chat_action(message.chat.id, 'typing')
    if message.from_user.username != "Channel_Bot":
        get_jrrp = jrrp.jrrp_get(message.from_user.id)
        bot.reply_to(message, "你今天的人品是: *{0}*\n{1}".format(get_jrrp,jrrp.jrrp_text(get_jrrp)))
    else:
        get_jrrp = jrrp.jrrp_get(message.sender_chat.id)
        bot.reply_to(message, "你今天的人品是: *{0}*\n{1}".format(get_jrrp,jrrp.jrrp_text(get_jrrp)))


@bot.message_handler(commands=['gu'])
def send_gu(message):
    try:
        path_file_name_wjj=os.listdir("./img/") #获取当前文件夹下个数
        path_file_name=glob.glob(pathname=f'./img/{path_file_name_wjj[random.randint(0,len(path_file_name_wjj)-1)]}/*.webp') #获取当前文件夹下个数
        sti = open(path_file_name[random.randint(0,len(path_file_name)-1)], 'rb')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
        sti.close()
    except Exception as errr:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '呜呜呜....图片没上传及时.......')
        traceback.print_exc()

@bot.message_handler(commands=['guhhsh'])
def send_nbnhhsh(message):
    try:
        text_rl = get_zl_text(message.text)
        if text_rl != False:
            bot.send_chat_action(message.chat.id, 'typing')
            hhsh_text_go = bot.reply_to(message,'正在查询请稍后...')
            text = hhsh.nbnhhsh(text_rl)
            bot.edit_message_text(text,hhsh_text_go.chat.id, hhsh_text_go.message_id)
            #bot.reply_to(message,zhihu_text)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"你的指令出错了惹!\n(缺少参数/guhhsh [查询拼音首字母缩写释义的文本])")
    except:
        pass

@bot.message_handler(commands=['moetrace'])
def gudlsoundcloud(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        jsonjx = json.loads(json.dumps(message.json))
        try:
            file_info = bot.get_file(jsonjx['reply_to_message']['photo'][-1]['file_id'])
        except:
            bot.reply_to(message, "呜呜呜...请使用 /moetrace 回复一张图片 ")
            return None
        botjson = bot.reply_to(message, "咕小酱正在获取图片请稍后....")

        #file = requests.get(
        #    'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))

        if bot_config['proxybool'] == True:
            botph = bot_config['proxy']
        else:
            botph = None

        get_info_about = requests.get("https://api.trace.moe/me",proxies=botph).json()

        bot.edit_message_text("咕小酱正在努力搜索中...", botjson.chat.id, botjson.message_id)

        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_config["botToken"], file_info.file_path),proxies=botph)

        #get_info = requests.get("https://api.trace.moe/search?cutBorders&anilistInfo&url={}".format(urllib.parse.quote_plus(url)),proxies=botph).json()

        get_info = requests.post("https://api.trace.moe/search?cutBorders&anilistInfo",
        files={"image": file.content}
        ,proxies=botph).json()

        get_title_jp = get_info["result"][0]["anilist"]["title"]["native"] 
        get_title_en = get_info["result"][0]["anilist"]["title"]["english"]

        get_title = "「"+str(get_title_jp)+"」("+str(get_title_en)+")"

        get_similarity = round(get_info["result"][0]["similarity"]*100,2)

        get_video = get_info["result"][0]["video"]
        
        quota = get_info_about["quota"]
        quotaUsed = get_info_about["quotaUsed"]
        quota_text = str(quota-(quotaUsed+1))

        
        if get_similarity >= 85:
            bot.edit_message_text("搜索信息如下↓ \n图片来自番剧: \n *"+str(get_title)+"* \n相似度: *"+str(get_similarity)+"* %\n查询额度还有: *"+str(quota_text)+"* 次", botjson.chat.id, botjson.message_id)
            bot.send_video_note(botjson.chat.id, get_video,reply_to_message_id=botjson.message_id)
        else:
            bot.edit_message_text("搜索信息如下↓ \n图片来自番剧: \n *"+str(get_title)+"* \n相似度: *"+str(get_similarity)+"* %\n查询额度还有: *"+str(quota_text)+"* 次\n预览视频因为 *相似度* 小于等于 *85%* 不予展示", botjson.chat.id, botjson.message_id)


    except Exception as oooo:
        bot.send_chat_action(message.chat.id, 'typing')
        # bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
        chatjson_img = bot.reply_to(message, '呜呜呜...咕小酱遇到了严重问题......\n错误日志: ' + str(oooo))
        time.sleep(3)
        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['httpcat'])
def httpcat(message):
    if get_zl_text(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 */httpcat [Http代码]*)")
    else:
        try:
            if bot_config['proxybool'] == True:
                botph = bot_config['proxy']
            else:
                botph = None
            text_rl = get_zl_text(message.text)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            try:
                chatjson_img = bot.send_photo(message.chat.id, "https://http.cat/"+str(text_rl),reply_to_message_id=message.message_id)
            except:
                chatjson_img = bot.send_photo(message.chat.id, "https://http.cat/404",reply_to_message_id=message.message_id)
        except Exception as boterr:
            #traceback.print_exc()
            bot.send_chat_action(message.chat.id, 'typing')
            #bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            #chatjson_img = bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr))
            chatjson_img = bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+traceback.format_exc())
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['guosu_std_mini'])
def osu_std_mini(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_std_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"std",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_std_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"std",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"std",True,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_taiko_mini'])
def osu_taiko_mini(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_taiko_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"taiko",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_taiko_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"taiko",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"taiko",True,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_catch_mini'])
def osu_catch_mini(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"catch",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"catch",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"catch",True,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_mania_mini'])
def osu_mania_mini(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_mania_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"mania",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_mania_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"mania",True,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"mania",True,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_std'])
def osu_std(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_std [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"std",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_std [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"std",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"std",False,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_taiko'])
def osu_taiko(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_taiko [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"taiko",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_taiko [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"taiko",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"taiko",False,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_catch'])
def osu_catch(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"catch",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_catch_mini [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"catch",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"catch",False,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_mania'])
def osu_mania(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_mania [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"mania",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_mania [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                osu_img_bool =  osu.get_osu_img(get_osu_id,"mania",False,message.from_user.id)
                if osu_img_bool:
                    sti = open('./tmp/'+osu_img_bool, 'rb')
                    bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                    sti.close()
                    os.remove('./tmp/'+osu_img_bool)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                else:
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                    chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                    time.sleep(5)
                    bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            osu_img_bool =  osu.get_osu_img(get_json["user_id"],"mania",False,message.from_user.id)
            if osu_img_bool:
                sti = open('./tmp/'+osu_img_bool, 'rb')
                bot.send_photo(message.chat.id, sti,reply_to_message_id=message.message_id)
                sti.close()
                os.remove('./tmp/'+osu_img_bool)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
            else:
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
                chatjson_out = bot.reply_to(message,"查询图片生成出错,请重试=-=")
                time.sleep(5)
                bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)
        except:
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)

@bot.message_handler(commands=['guosu_bind'])
def osu_bind(message):
    if message.from_user.username != "Channel_Bot":
        get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
        if get_osu_id is not False:
            get_osu_name = osu.get_osuid(get_osu_id)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"您已经绑定了 *"+str(get_osu_name["username"])+"* \n 如需解绑请使用 */guosu_unbind* 指令")
            return None
    else:
        get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
        if get_osu_id is not False:
            get_osu_name = osu.get_osuid(get_osu_id)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"您已经绑定了 *"+str(get_osu_name["username"])+"* \n 如需解绑请使用 */guosu_unbind* 指令")
            return None

    if get_zl_text(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 */guosu_bind [ID/用户名]* 来绑定)")
    else:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is not False:
                get_osu_name = osu.get_osuid(get_osu_id)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"您已经绑定了 *"+str(get_osu_name["username"])+"* \n 如需解绑请使用 */guosu_unbind* 指令")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_bind = bot.reply_to(message,"正在绑定...")
                try:
                    get_osu_id = osu.get_osuid(get_zl_text(message.text))
                    if osu.sql_osu2tg_id(get_osu_id["user_id"]) is False:
                        osu.sql_wq(message.from_user.id,get_osu_id["user_id"])
                        bot.edit_message_text("*绑定成功!*",chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                    else:
                        bot.edit_message_text("抱歉,该 OSU ID 已经绑定其他 Telegram ID,如需绑定请联系机器人管理员!",chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                except Exception as err:
                    bot.edit_message_text("*绑定失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_bind.chat.id, chatjson_bind.message_id)
                    time.sleep(10)
                    bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is not False:
                get_osu_name = osu.get_osuid(get_osu_id)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"您已经绑定了 *"+str(get_osu_name["username"])+"* \n 如需解绑请使用 */guosu_unbind* 指令")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_bind = bot.reply_to(message,"正在绑定...")
                try:
                    get_osu_id = osu.get_osuid(get_zl_text(message.text))
                    if osu.sql_osu2tg_id(get_osu_id["user_id"]) is False:
                        osu.sql_wq(message.sender_chat.id,get_osu_id["user_id"])
                        bot.edit_message_text("*绑定成功!*",chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                    else:
                        bot.edit_message_text("抱歉,该 OSU ID 已经绑定其他 Telegram ID,如需绑定请联系机器人管理员!",chatjson_bind.chat.id, chatjson_bind.message_id)
                        time.sleep(10)
                        bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
                except Exception as err:
                    bot.edit_message_text("*绑定失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_bind.chat.id, chatjson_bind.message_id)
                    time.sleep(10)
                    bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)

@bot.message_handler(commands=['guosu_unbind'])
def osu_unbind(message):
        get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
        if get_osu_id is False:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"您未绑定 OSU ID \n 如需绑定请使用 */guosu_bind [ID/用户名]* 指令")
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            chatjson_bind = bot.reply_to(message,"正在解除绑定...")
            
            if osu.sql_del(message.from_user.id) is False:
                osu.sql_wq(message.from_user.id,get_osu_id["user_id"])
                bot.edit_message_text("*解绑失败*,请联系机器人管理员!",chatjson_bind.chat.id, chatjson_bind.message_id)
                time.sleep(10)
                bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)
            else:
                bot.edit_message_text("*解绑成功!*",chatjson_bind.chat.id, chatjson_bind.message_id)
                time.sleep(10)
                bot.delete_message(chatjson_bind.chat.id, chatjson_bind.message_id)


@bot.message_handler(commands=['guosu_played'])
def osu_played(message):
    if get_zl_text(message.text) == False:
        if message.from_user.username != "Channel_Bot":
            get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_played [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                try:
                    get_osu_new_info = osu.get_osu_new_played(get_osu_id)
                    get_osu_map_json = osu.get_osu_beatmaps(get_osu_new_info["beatmap_id"])
                except:
                    bot.edit_message_text("*查询失败*,没有查询到您的最近游玩记录!",chatjson_out.chat.id, chatjson_out.message_id)
                    return None

                try:
                    get_pp = str(get_osu_new_info["pp"])
                except:
                    get_pp = "暂不可用"

                out_text = f"*最新游玩成绩*\n *{get_osu_map_json['title_unicode']} - {get_osu_map_json['artist_unicode']}*\n获得PP: *{get_pp}*\n评级: *{get_osu_new_info['rank']}*\n分数: *{get_osu_new_info['score']}*\n最大连击数: *{get_osu_new_info['maxcombo']}*"
                out_text +=f"\n300G: *{get_osu_new_info['countgeki']}*\n300: *{get_osu_new_info['count300']}*\n100K: *{get_osu_new_info['countkatu']}*\n100: *{get_osu_new_info['count100']}*\n50: *{get_osu_new_info['count50']}*\nMiss: *{get_osu_new_info['countmiss']}*\n"
                out_text +=f"游玩时间: *{osu.time_cn(get_osu_new_info['date'])}*"
                bot.edit_message_text(out_text,chatjson_out.chat.id, chatjson_out.message_id)
        else:
            get_osu_id = osu.sql_tg2osu_id(message.sender_chat.id)
            if get_osu_id is False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜...指令有问题\n(缺少参数 */guosu_mania [OSU ID/用户名]* )")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
                try:
                    get_osu_new_info = osu.get_osu_new_played(get_osu_id)
                    get_osu_map_json = osu.get_osu_beatmaps(get_osu_new_info["beatmap_id"])
                except:
                    bot.edit_message_text("*查询失败*,没有查询到您的最近游玩记录!",chatjson_out.chat.id, chatjson_out.message_id)
                    return None
                try:
                    get_pp = str(get_osu_new_info["pp"])
                except:
                    get_pp = "暂不可用"

                out_text = f"*最新游玩成绩*\n{get_osu_map_json['title_unicode']} - {get_osu_map_json['artist_unicode']}\n获得PP: *{get_pp}*\n评级: *{get_osu_new_info['rank']}*\n分数: *{get_osu_new_info['score']}*\n最大连击数: *{get_osu_new_info['maxcombo']}*"
                out_text +=f"\n300G: *{get_osu_new_info['countgeki']}*\n300: *{get_osu_new_info['count300']}*\n100K: *{get_osu_new_info['countkatu']}*\n100: *{get_osu_new_info['count100']}*\n50: *{get_osu_new_info['count50']}*\nMiss: *{get_osu_new_info['countmiss']}*\n"
                out_text +=f"游玩时间: *{osu.time_cn(get_osu_new_info['date'])}*"
                bot.edit_message_text(out_text,chatjson_out.chat.id, chatjson_out.message_id)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        chatjson_out = bot.reply_to(message,"正在查询,请稍后...")
        try:
            get_json = osu.get_osuid(get_zl_text(message.text))
            try:
                get_osu_new_info = osu.get_osu_new_played(get_json["user_id"])
                get_osu_map_json = osu.get_osu_beatmaps(get_osu_new_info["beatmap_id"])
            except:
                bot.edit_message_text("*查询失败*,没有查询到此玩家的最近游玩记录!",chatjson_out.chat.id, chatjson_out.message_id)
                return None

            try:
                get_pp = str(get_osu_new_info["pp"])
            except:
                get_pp = "暂不可用"

            out_text = f"*最新游玩成绩*\n{get_osu_map_json['title_unicode']} - {get_osu_map_json['artist_unicode']}\n获得PP: *{get_pp}*\n评级: *{get_osu_new_info['rank']}*\n分数: *{get_osu_new_info['score']}*\n最大连击数: *{get_osu_new_info['maxcombo']}*"
            out_text +=f"\n300G: *{get_osu_new_info['countgeki']}*\n300: *{get_osu_new_info['count300']}*\n100K: *{get_osu_new_info['countkatu']}*\n100: *{get_osu_new_info['count100']}*\n50: *{get_osu_new_info['count50']}*\nMiss: *{get_osu_new_info['countmiss']}*\n"
            out_text +=f"游玩时间: *{osu.time_cn(get_osu_new_info['date'])}*"
            bot.edit_message_text(out_text,chatjson_out.chat.id, chatjson_out.message_id)

           
        except Exception as err:
            traceback.print_exc()
            bot.edit_message_text("*查询失败*,请检查 OSU ID 是否正确或者联系机器人管理员!",chatjson_out.chat.id, chatjson_out.message_id)
            time.sleep(10)
            bot.delete_message(chatjson_out.chat.id, chatjson_out.message_id)



@bot.message_handler(commands=['guosu_help'])
def osu_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message,"""
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

@bot.message_handler(commands=['guip_traceroute'])
def guip_traceroute(message):
    #bot.reply_to(message,"此功能功能暂不开放")
    #return None
    input_ip = get_zl_text(message.text)
    if input_ip is False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 */guip_traceroute [ip]*)")
        return None

    get_lo = guip.is_localhost_ip(input_ip)

    if get_lo is True:
        bot.reply_to(message,"呜呜呜...咕小酱发现此 *地址* 为 *本地主机* 地址,无法检测")
        return None

    bot.send_chat_action(message.chat.id, 'typing')
    chatjson_ip = bot.reply_to(message,"正在进行路由跟踪...")
    get_gu = guip.gu_traceroute(input_ip)
    if get_gu is False:
        bot.edit_message_text("呜呜呜...咕小酱无法访问此 *地址* 或者 这个地址就根本 *不存在* !",chatjson_ip.chat.id, chatjson_ip.message_id)
        return None
    
    bot.edit_message_text(f"跟踪信息如下:\n```\n{get_gu}\n```",chatjson_ip.chat.id, chatjson_ip.message_id)

@bot.message_handler(commands=['guip_ping'])
def guip_ping(message):
    input_ip = get_zl_text(message.text)
    if input_ip is False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 */guip_ping [ip]*)")
        return None

    get_lo = guip.is_localhost_ip(input_ip)

    if get_lo is True:
        bot.reply_to(message,"呜呜呜...咕小酱发现此 *地址* 为 *本地主机* 地址,无法检测")
        return None

    bot.send_chat_action(message.chat.id, 'typing')
    chatjson_ip = bot.reply_to(message,"正在进行 Ping ...")
    get_gu = guip.gu_ping(input_ip)
    if get_gu is False:
        bot.edit_message_text("呜呜呜...咕小酱无法Ping通此 *地址* 或者 这个地址就根本 *不存在* !",chatjson_ip.chat.id, chatjson_ip.message_id)
        return None
    
    bot.edit_message_text(f"Ping 信息如下:\n```\n{get_gu}\n```",chatjson_ip.chat.id, chatjson_ip.message_id)


@bot.message_handler(commands=['gu_eat'])
def gu_eat(message):
    #print(message)
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
        
    except Exception as err:
        bot.reply_to(message, "呜呜呜...咕小酱获取不到此人的头像 ")
        bot.delete_message(del_json.chat.id, del_json.message_id)
        return None
    
    if bot_config['proxybool'] == True:
            botph = bot_config['proxy']
    else:
        botph = None

    get_info_about = requests.get("https://api.trace.moe/me",proxies=botph).json()

    r = requests.get(img_url, stream=True,proxies=botph)
    out_file_name = f"gu_eat_{user_id}.png"
    if r.status_code == 200:
        open(f'./tmp/{out_file_name}', 'wb').write(r.content)

    out_rl = make_img.make_eat_img(f'{out_file_name}',str(user_id))

    try:
        sti = open(out_rl, 'rb')
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
        bot.delete_message(del_json.chat.id, del_json.message_id)
        sti.close()
        os.remove(out_rl)
        os.remove(f'./tmp/{out_file_name}')
    except Exception as errr:
        bot.delete_message(del_json.chat.id, del_json.message_id)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '呜呜呜....图片没上传及时.......')
        traceback.print_exc()
    

@bot.message_handler(commands=['gu_5000choyen'])
def gu_5000choyen(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        get_text = get_zl_text(message.text)
        if get_text == False:
            bot.reply_to(message, "呜呜呜...请使用 */gu_5000choyen* (上半句)|(下半句) 来生成图片 ")
            return None
        keyword = get_text
        del_json = bot.reply_to(message, "咕小酱正在努力生成请稍后...")
        if '｜' in keyword:
            keyword=keyword.replace('｜','|')
        elif '|' in keyword:
            pass
        else:
            bot.reply_to(message, "未检测到分句 格式 (上半句)|(下半句)")
            return None
        if message.from_user.username != "Channel_Bot":
            file_id= message.from_user.id
        else:
            file_id= message.sender_chat.id
        upper=keyword.split("|")[0]
        downer=keyword.split("|")[1]
        bot.send_chat_action(message.chat.id, 'choose_sticker')
        img=genImage(word_a=upper, word_b=downer)
        img.save(f"./tmp/temp{file_id}.png")
        sti = open(f"./tmp/temp{file_id}.png", 'rb')
        bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
        bot.delete_message(del_json.chat.id, del_json.message_id)
        sti.close()
        os.remove(f"./tmp/temp{file_id}.png")
    except:
         bot.reply_to(message, "呜呜呜...生成图片错误了惹,请尝试重新生成...")

@bot.inline_handler(lambda query: query.query == 'jrrp')
def query_jrrpt(inline_query):
    try:
        #print("jrrp=",inline_query)
        localtime = time.localtime(time.time())
        markup = types.InlineKeyboardMarkup()
        get_jrrp = jrrp.jrrp_get(inline_query.from_user.id)
        btn1 = types.InlineKeyboardButton("我也试试", switch_inline_query="jrrp")
        markup.add(btn1)
        r = types.InlineQueryResultArticle('1', f'今日人品 {localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}', types.InputTextMessageContent("你今天的人品是: {0}\n{1}".format(get_jrrp,jrrp.jrrp_text_init(get_jrrp))),thumb_url="https://s3.bmp.ovh/imgs/2022/07/02/e15481817c097493.jpg",description="测测你今天的人品!",reply_markup=markup)
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception as e:
        traceback.print_exc()

@bot.inline_handler(lambda query: True)
def query_mr(inline_query):
    try:
        #print(inline_query)
        localtime = time.localtime(time.time())
        markup = types.InlineKeyboardMarkup()
        get_jrrp = jrrp.jrrp_get(inline_query.from_user.id)
        btn1 = types.InlineKeyboardButton("我也试试", switch_inline_query="jrrp")
        markup.add(btn1)
        r = types.InlineQueryResultArticle('5', f'今日人品 {localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}', types.InputTextMessageContent("你今天的人品是: {0}\n{1}".format(get_jrrp,jrrp.jrrp_text_init(get_jrrp))),thumb_url="https://s3.bmp.ovh/imgs/2022/07/02/e15481817c097493.jpg",description="测测你今天的人品!",reply_markup=markup)
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception as e:
        traceback.print_exc()

#Main   
if __name__ == '__main__':
    while True:
        try:
            #logger = telebot.logger
            #telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
            logger.info(f"启动成功!")
            bot.polling()
            

        except Exception as err:
            logger.error(f"遇到错误正在重启:")
            traceback.print_exc()
        time.sleep(1)