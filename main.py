# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from lxml import etree
from decimal import Decimal
from ping3 import ping
from loguru import logger
import sqlite3
import requests
import sys
import zipfile
import telebot
import json
import os
import time
import yaml
import random
import os.path
import glob
import re
import hashlib
import eyed3


if os.path.exists("./config.yml") == False: # 初始化Bot
    logger.info(f"开始第一次初始化")
    logger.info(f"创建 config.yml 配置文件")
    with open("./config.yml", 'wb') as f:
        f.write(bytes("botToken: \nosuToken: \nproxybool: False\nproxy: {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'}",'utf-8'))
        f.close()
    logger.info(f"创建文件夹")
    dir_list = ["./img","./tmp","./user","./user/jrrp"]
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
    logger.info(f"初始化原神系统")
    import pool_data
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
    else:
        bot = telebot.TeleBot(bot_config["botToken"])
        if bot_config["proxybool"] == True:
            from telebot import apihelper
            apihelper.proxy = bot_config['proxy']
        logger.info(f"配置文件加载完毕!")
        from gacha import gacha_info , FILE_PATH , Gacha , POOL ,DEFAULT_POOL
        from gachacz import gacha_info_cz , Gacha_cz

def get_random():
    url='https://www.random.org/integers/?num=1&min=0&max=100&col=1&base=10&format=plain&rnd=new'
    if bot_config['proxybool'] == True:
        proxies = bot_config['proxy']
        res = requests.get(url, proxies=proxies)
    else:
        res = requests.get(url)
    return res.text

def jrrp_text(nub_in):
        nub = int(nub_in)
        if nub >= 90:
            return "人品好评！"
        elif nub >= 70:
            return "www,人品还挺好的("
        elif nub >= 60:
            return "人品还过得去..."
        elif nub >= 40:
            return "还好还好只有" + str(nub)
        elif nub >= 20:
            return "这数字太....要命了"
        elif nub >= 1:
            return "啊这人品"

def fill_json(id): #让我康康你的数据文件在不在?
        if os.path.isfile('./user/jrrp/'+str(id)+'.json') == True:
            return True
        else:
            return False

@bot.message_handler(commands=['jrrp'])
def send_jrrp(message):
    try:
        if fill_json(message.from_user.id) == False:
            #print('创建用户储存文件')
            file = open('./user/jrrp/'+str(message.from_user.id)+'.json','w')
            jrrpp = get_random()
            data1 = {
            'jrrp' : jrrpp,
            'time' : time.strftime("%d", time.localtime())
                    }
            file.write(json.dumps(data1))
            file.close()
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, "你今天的人品是："+str(jrrpp)+'\n'+jrrp_text(jrrpp))
        else:
            with open('./user/jrrp/'+str(message.from_user.id)+'.json', 'r') as timejrrp:
                bottok = eval(json.loads(json.dumps(str(timejrrp.read()))))
                if time.strftime("%d", time.localtime()) == bottok['time']:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message, "你今天的人品是："+str(bottok['jrrp'])+'\n'+jrrp_text(bottok['jrrp']))
                else:
                    file = open('./user/jrrp/'+str(message.from_user.id)+'.json','w')
                    jrrpp = get_random()
                    data1 = {
                        'jrrp' : jrrpp,
                        'time' : time.strftime("%d", time.localtime())
                            }
                    file.write(json.dumps(data1))
                    file.close()
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message, "你今天的人品是："+str(jrrpp)+'\n'+jrrp_text(jrrpp))
    except Exception as errr:
        bot.send_chat_action(message.chat.id, 'typing')
        if os.path.isfile('./user/jrrp/'+str(message.from_user.id)+'.json') == True:
            os.remove('./user/jrrp/'+str(message.from_user.id)+'.json')
        bot.reply_to(message, '呜呜呜....今日人品出错了,请重新发送 /jrrp \n错误日志: '+str(errr))


@bot.message_handler(commands=['gugetup10'])
def send_ck(message):
    G = Gacha()
    json_out_ten = G.gacha_10(tggid=message.from_user.id)
    outtt = json.loads(json.dumps(json_out_ten))
    bot.send_chat_action(message.chat.id, 'typing')
    text = bot.reply_to(message,outtt["msg"])
    sti = open(outtt["fil"], 'rb')
    bot.send_chat_action(message.chat.id, 'upload_photo')
    bot.send_photo(message.chat.id,sti.read(),reply_to_message_id=text.message_id)
    sti.close()
    os.remove(outtt["fil"])
    
@bot.message_handler(commands=['gugetcz10'])
def send_ck(message):
    G = Gacha_cz()
    json_out_ten = G.gacha_10(tggid=message.from_user.id)
    outtt = json.loads(json.dumps(json_out_ten))
    bot.send_chat_action(message.chat.id, 'typing')
    text = bot.reply_to(message,outtt["msg"])
    sti = open(outtt["fil"], 'rb')
    bot.send_chat_action(message.chat.id, 'upload_photo')
    bot.send_photo(message.chat.id,sti.read(),reply_to_message_id=text.message_id)
    sti.close()
    os.remove(outtt["fil"])

@bot.message_handler(commands=['gugetup'])
def send_ck(message):
    G = Gacha()
    text = bot.reply_to(message,gacha_info())

@bot.message_handler(commands=['gugetcz'])
def send_ck(message):
    G = Gacha()
    text = bot.reply_to(message,gacha_info_cz())


if __name__ == '__main__':
    while True:
        try:
            logger.info(f"启动成功!")
            bot.polling()
        except Exception as err:
            logger.error(f"遇到错误正在重启:"+str(err))
        time.sleep(1)