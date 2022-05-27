import telebot
import zipfile
import yaml
from loguru import logger
import os.path
import requests
import sys
import time
import json
#额外
import jrrp


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
#命令
@bot.message_handler(commands=['jrrp'])
def send_jrrp(message):
    bot.send_chat_action(message.chat.id, 'typing')
    get_jrrp = jrrp.jrrp_get(message.from_user.id)
    bot.reply_to(message, "你今天的人品是: *{0}*\n{1}".format(get_jrrp,jrrp.jrrp_text(get_jrrp)))


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