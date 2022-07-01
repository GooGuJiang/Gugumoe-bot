import telebot
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
#额外
import jrrp
import hhsh
import guip

if os.path.exists("./config.yml") is False: # 初始化Bot
    logger.info(f"开始第一次初始化")
    logger.info(f"创建 config.yml 配置文件")
    with open("./config.yml", 'wb') as f:
        f.write(bytes("botToken: \nosuToken: \nproxybool: False\nproxy: {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'}\napikey: \nmusicapi: \nmusicphone: \nmusicpwd: ",'utf-8'))
        f.close()
    logger.info(f"创建文件夹")
    dir_list = ["./img","./tmp","./user","./user/jrrp","./user/shoutmp","./user/osu"]
    for i in range(0,len(dir_list)):
        if os.path.exists(dir_list[i]) == False:
            logger.info(f"正在创建 "+str(dir_list[i]))
            os.mkdir(dir_list[i])
        else:
            logger.info(f"已存在"+str(dir[i]))
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
    #elif bot_config["osuToken"] == None:
        #logger.error(f"配置文件 osuToken 未填写")
        #sys.exit()
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
    bot.send_chat_action(message.chat.id, 'typing')
    get_jrrp = jrrp.jrrp_get(message.from_user.id)
    bot.reply_to(message, "你今天的人品是: *{0}*\n{1}".format(get_jrrp,jrrp.jrrp_text(get_jrrp)))

@bot.message_handler(commands=['gu'])
def send_gu(message):
    try:
        path_file_name=glob.glob(pathname='./img/*.webp') #获取当前文件夹下个数
        sti = open(path_file_name[random.randint(0,len(path_file_name)-1)], 'rb')
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_sticker(message.chat.id, sti,reply_to_message_id=message.message_id)
        sti.close()
    except Exception as errr:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, '呜呜呜....图片没上传及时.......')
        print(errr)

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
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /httpcat *[Http代码]*)")
    else:
        try:
            if bot_config['proxybool'] == True:
                botph = bot_config['proxy']
            else:
                botph = None
            text_rl = get_zl_text(message.text)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            try:
                chatjson_img = bot.send_photo(message.chat.id, "https://http.cat/"+str(text_rl),reply_to_message_id=message.message_id,proxies=botph)
            except:
                chatjson_img = bot.send_photo(message.chat.id, "https://http.cat/404",reply_to_message_id=message.message_id,proxies=botph)
        except Exception as boterr:
            #print(boterr)
            bot.send_chat_action(message.chat.id, 'typing')
            #bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            chatjson_img = bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr))
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['guosu_std_mini'])
def osu_std_mini(message):
    if get_zl_text(message.text) == False:
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
    get_osu_id = osu.sql_tg2osu_id(message.from_user.id)
    if get_osu_id is not False:
        get_osu_name = osu.get_osuid(get_osu_id)
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"您已经绑定了 *"+str(get_osu_name["username"])+"* \n 如需解绑请使用 */guosu_unbind* 指令")
        return None

    if get_zl_text(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 */guosu_bind [ID/用户名]* 来绑定)")
    else:
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
            except:
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
*/guosu_bind 绑定 OSU ID*
*/guosu_unbind 解除绑定 OSU ID*
*/guosu_help 查看本帮助*
""")

@bot.message_handler(commands=['guip_traceroute'])
def guip_traceroute(message):
    input_ip = get_zl_text(message.text)
    if input_ip is False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /guip_traceroute *[ip]*)")
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
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /guip_ping *[ip]*)")
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
        

#Main   
if __name__ == '__main__':
    while True:
        try:
            #logger = telebot.logger
            #telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
            logger.info(f"启动成功!")
            bot.polling()
            

        except Exception as err:
            logger.error(f"遇到错误正在重启:"+str(err))
        time.sleep(1)