import telebot
import zipfile
import yaml
from loguru import logger
import os.path
import requests
import sys
import time
import json
import glob
import random
#额外
import jrrp
import hhsh

if os.path.exists("./config.yml") == False: # 初始化Bot
    logger.info(f"开始第一次初始化")
    logger.info(f"创建 config.yml 配置文件")
    with open("./config.yml", 'wb') as f:
        f.write(bytes("botToken: \nosuToken: \nproxybool: False\nproxy: {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'}\napikey: \nmusicapi: \nmusicphone: \nmusicpwd: ",'utf-8'))
        f.close()
    logger.info(f"创建文件夹")
    dir_list = ["./img","./tmp","./user","./user/jrrp","./user/shoutmp"]
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
        #    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_config["botToken"], file_info.file_path),proxies=bot_config['proxy'])
            botph = bot_config['proxy']
        else:
        #    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_config["botToken"], file_info.file_path))
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