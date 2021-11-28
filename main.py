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

def nbnhhsh(text):
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }

    data = {
        "text": text
    }

    response = requests.post(url=url, headers=headers, data=data)
    json_text = response.text
    ok_json = eval(json.dumps(json.loads(json_text)))
    try:
        sc = ok_json[0]["trans"]
        gu_text = '缩写释义文本:'+ok_json[0]["name"]+'\n\n你查询的可能是:\n'
        for i in range(0, len(sc)):
            if len(sc) != i:
                gu_text += str(i+1)+'.『'+ok_json[0]["trans"][i]+'』\n'
            else:
                gu_text += str(i+1)+'.『'+ok_json[0]["trans"][i]+'』'
        return gu_text
    except:
        return "无查询结果"

def howpingip(textlt): #指令提取
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



@bot.message_handler(commands=['guhhsh'])
def send_nbnhhsh(message):
    try:
        text_rl = howpingip(message.text)
        if text_rl != False:
            bot.send_chat_action(message.chat.id, 'typing')
            hhsh_text_go = bot.reply_to(message,'正在查询请稍后...')
            text = nbnhhsh(text_rl)
            bot.edit_message_text(text,hhsh_text_go.chat.id, hhsh_text_go.message_id)
            #bot.reply_to(message,zhihu_text)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"你的指令出错了惹!\n(缺少参数/guhhsh [查询拼音首字母缩写释义的文本])")
    except:
        pass

#@bot.message_handler(commands=['guyshow'])
#def send_whathow(message):
#    text_rl = howpingip(message.text)
#    if text_rl != False:
#        bot.send_chat_action(message.chat.id, 'typing')
#        hhsh_text_go = bot.reply_to(message,'正在查询请稍后...')
#        text = get_resource_map_mes(text_rl)
#        bot.edit_message_text(text,hhsh_text_go.chat.id, hhsh_text_go.message_id)
#    else:
#        bot.send_chat_action(message.chat.id, 'typing')
#        bot.reply_to(message,"你的指令出错了惹!\n(缺少参数/guyshow [资源位置])")

if __name__ == '__main__':
    while True:
        try:
            logger.info(f"启动成功!")
            bot.polling()
        except Exception as err:
            logger.error(f"遇到错误正在重启:"+str(err))
        time.sleep(1)