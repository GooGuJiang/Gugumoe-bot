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
from telebot import types
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
import urllib.parse

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
        bot = telebot.TeleBot(bot_config["botToken"])
        if bot_config["proxybool"] == True:
            from telebot import apihelper
            apihelper.proxy = bot_config['proxy']
        logger.info(f"配置文件加载完毕!")

def dl_netmusic_info(mid): #网易云音乐信息获取
    try:
        son_info_get = requests.get(str(bot_config["musicapi"])+"/song/detail?ids="+str(mid))
        son_info_json= json.loads(json.dumps(json.loads(str(son_info_get.text))))
        son_name = son_info_json["songs"][0]["name"]
        #作者信息拼接
        son_art_json =  son_info_json["songs"][0]["ar"]
        son_art_text = ''
        for i in range(0,len(son_art_json)):
            if len(son_art_json) == 0:
                son_art_text += son_info_json["songs"][0]["ar"][i]["name"]
            else:
                if i == len(son_art_json)-1:
                    son_art_text += son_info_json["songs"][0]["ar"][i]["name"]
                else:
                    son_art_text += son_info_json["songs"][0]["ar"][i]["name"]+","
        jsonout = {
            "success":"ok",
            "muname":son_name,
            "art":str(son_art_text)
            }
        return jsonout
    except Exception as ooow:
        return {"success":"err","err":str(ooow)}

def dl_netmusic(mid,pwt): #网易云音乐下载!
    try:
        denlu = requests.get(str(bot_config["musicapi"])+"/login/cellphone?phone="+str(bot_config["musicphone"])+"&password="+str(bot_config["musicpwd"]))#获取登录信息
        inp_cookjson = json.loads(json.dumps(json.loads(str(denlu.text))))
        url=str(bot_config["musicapi"])+'/song/url?id='+str(mid)+'&cookie='+inp_cookjson["cookie"]
        res= requests.get(url)
        dljson = json.dumps(json.loads(str(res.text)))
        outjson = json.loads(dljson)
        if outjson["data"][0]["url"] == None: #检测音乐地址
            return False
        res = requests.get(outjson["data"][0]["url"])
        with open("./tmp/"+str(outjson["data"][0]["id"])+'.'+str(outjson["data"][0]["type"]), 'wb') as f:
            f.write(res.content)
        time.sleep(0.5)
        son_info_get = requests.get(str(bot_config["musicapi"])+"/song/detail?ids="+str(mid))
        son_info_json= json.loads(json.dumps(json.loads(str(son_info_get.text))))
        son_name = son_info_json["songs"][0]["name"]
        #作者信息拼接
        son_art_json =  son_info_json["songs"][0]["ar"]
        son_art_text = ''
        for i in range(0,len(son_art_json)):
            if len(son_art_json) == 0:
                son_art_text += son_info_json["songs"][0]["ar"][i]["name"]
            else:
                if i == len(son_art_json)-1:
                    son_art_text += son_info_json["songs"][0]["ar"][i]["name"]
                else:
                    son_art_text += son_info_json["songs"][0]["ar"][i]["name"]+","
        if str(outjson["data"][0]["type"]) == "mp3":
            #下载专辑封面
            dl_img = requests.get(son_info_json["songs"][0]["al"]["picUrl"])
            with open("./tmp/"+str(mid)+'.jpg', 'wb') as f:
                f.write(dl_img.content)
            #音乐信息写入
            audiofile = eyed3.load("./tmp/"+str(outjson["data"][0]["id"])+'.'+str(outjson["data"][0]["type"]))
            #audiofile.initTag()
            audiofile.tag.images.set(3, open("./tmp/"+str(mid)+'.jpg','rb').read(), 'image/jpeg') #添加封面
            audiofile.tag.artist = str(son_art_text)
            audiofile.tag.album = son_info_json["songs"][0]["al"]["name"]  # 唱片集
            audiofile.tag.title = son_name  # 标题
            audiofile.tag.save() # 保存文件
            os.remove("./tmp/"+str(mid)+'.jpg')
        jsonout = {
            "success":"ok",
            "muname":son_name,
            "art":str(son_art_text),
            "fil":"./tmp/"+str(outjson["data"][0]["id"])+'.'+str(outjson["data"][0]["type"])
            }
        return jsonout
    except Exception as ooow:
        return {"success":"err","err":str(ooow)}

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

def getStrAsMD5(parmStr):
    if isinstance(parmStr,str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()

def dl_sdmusic_info(url_dl):
    try:
        # post参数合成区
        url = 'https://soundcloudmp3.cc/ajax.php'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }


        data =  {"action": "video_preview","vidURL": url_dl,"tType":"trim" }
        # post访问
        if bot_config['proxybool'] == True:
            response = requests.post(url=url, headers=headers, data=data,proxies=bot_config['proxy'])
        else:
            response = requests.post(url=url, headers=headers, data=data)
        page_text = json.loads(str(response.text))
        return page_text["vidTitle"]
    except Exception as ooo:
        print(ooo)
        return False


def dl_sdmusic(url_dl):
    try:
        # post参数合成区
        url = 'https://soundcloudmp3.cc/ajax.php'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }


        data =  {"action": "video_preview","vidURL": url_dl,"tType":"trim" }


        # post访问
        if bot_config['proxybool'] == True:
            response = requests.post(url=url, headers=headers, data=data,proxies=bot_config['proxy'])
        else:
            response = requests.post(url=url, headers=headers, data=data)
        page_text = json.loads(str(response.text))
        down_url = "https://soundcloudmp3.cc/"+page_text["vidSrc"][1:]
        if bot_config['proxybool'] == True:
            res = requests.get(down_url,proxies=bot_config['proxy'])
        else:
            res = requests.get(down_url)
        
        try:
            with open("./tmp/"+page_text["vidTitle"]+'.mp3', 'wb') as f:
                f.write(res.content)
        except:
            with open("./tmp/"+getStrAsMD5(page_text["vidTitle"])+'.mp3', 'wb') as f:
                f.write(res.content)
        #下载专辑图片
        dl_img = repr(page_text["vidImage"])
        dl_img = dl_img[1:len(dl_img)-1]
        if bot_config['proxybool'] == True:
            res = requests.get(dl_img,proxies=bot_config['proxy'])
        else:
            res = requests.get(dl_img)
        
        try:
            with open("./tmp/"+page_text["vidTitle"]+'.jpg', 'wb') as f:
                f.write(res.content)
        except:
            with open("./tmp/"+getStrAsMD5(page_text["vidTitle"])+'.jpg', 'wb') as f:
                f.write(res.content)

        #写入信息
        try:
            audiofile = eyed3.load("./tmp/"+page_text["vidTitle"]+'.mp3')  # 读取mp3文件
            audiofile.initTag()  # 初始化所有标签信息，将之前所有的标签清除
            audiofile.tag.images.set(3, open("./tmp/"+page_text["vidTitle"]+'.jpg','rb').read(), 'image/jpeg') #添加封面
            audiofile.tag.album = u"SoundCloud"  # 唱片集
            audiofile.tag.title = page_text["vidTitle"]  # 标题
            audiofile.tag.save() # 保存文件
            os.remove("./dl-tmp/"+page_text["vidTitle"]+'.jpg')
            fill = page_text["vidTitle"]
        except:
            audiofile = eyed3.load("./tmp/"+getStrAsMD5(page_text["vidTitle"])+'.mp3')
            audiofile.initTag()  # 初始化所有标签信息，将之前所有的标签清除
            audiofile.tag.images.set(3, open("./tmp/"+getStrAsMD5(page_text["vidTitle"])+'.jpg','rb').read(), 'image/jpeg') #添加封面
            audiofile.tag.album = u"SoundCloud"  # 唱片集
            audiofile.tag.title = page_text["vidTitle"]  # 标题
            audiofile.tag.save() # 保存文件
            os.remove("./dl-tmp/"+getStrAsMD5(page_text["vidTitle"])+'.jpg')
            fill = "./dl-tmp/"+getStrAsMD5(page_text["vidTitle"])
        
        return fill
    except Exception as ooo:
        print(ooo)
        return False

def is_sd_url(url):
    if re.match(r'^https*://(www.)*soundcloud\.com/', url) == None:
        return False
    else:
        return True

def is_163pc_url(url):
    if re.match(r'^https*://(music.)*163\.com/', url) == None:
        return False
    else:
        return True

def is_163ph_url(url):
    if re.match(r'^https*://(y.music.)*163\.com/', url) == None:
        return False
    else:
        return True
#--------------------------------------------------------------


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

@bot.message_handler(commands=['gudlsds'])
def gudlsoundcloud(message):
    if howpingip(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /gudlsds [SoundCloud音乐链接] 暂不支持列表下载)")
    else:
        try:
            text_rl = howpingip(message.text)
            if is_sd_url(text_rl) == True:
                bot.send_chat_action(message.chat.id, 'typing')
                chatjson_img = bot.reply_to(message,"正在从SoundCloud获取音乐信息请稍后....")
                info_music = dl_sdmusic_info(text_rl)
                chatjson_img = bot.edit_message_text("正在下载『"+info_music+"』请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                dl_muss = dl_sdmusic(text_rl)
                chatjson_img = bot.edit_message_text("正在上传『"+info_music+"』请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                bot.send_chat_action(message.chat.id, 'upload_audio')
                audio = open("./tmp/"+dl_muss+".mp3", 'rb')
                bot.send_audio(message.chat.id, audio)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.edit_message_text("『"+info_music+'』上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                time.sleep(3)
                bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                audio.close()
                os.remove("./tmp/"+dl_muss+".mp3")
        except Exception as boterr:
            #print(boterr)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['httpcat'])
def gudlsoundcloud(message):
    if howpingip(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /httpcat [Http代码])")
    else:
        try:
            text_rl = howpingip(message.text)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            try:
                chatjson_img = bot.send_photo(message.chat.id, "https://http.cat/"+str(text_rl),reply_to_message_id=message.message_id)
            except:
                chatjson_img = bot.send_photo(message.chat.id, "https://http.cat/404",reply_to_message_id=message.message_id)
        except Exception as boterr:
            #print(boterr)
            bot.send_chat_action(message.chat.id, 'typing')
            #bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            chatjson_img = bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr))
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['gubig'])
def gudlsoundcloud(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        jsonjx = json.loads(json.dumps(message.json))
        #print(jsonjx['reply_to_message']['photo'][2]['file_id'])
        try:
            file_info = bot.get_file(jsonjx['reply_to_message']['photo'][2]['file_id'])
        except:
            bot.reply_to(message,"请回复一张图片,不然放大什么?")
            return None
        botjson = bot.reply_to(message,"正在获取图片请稍后....")
        if bot_config['proxybool'] == True:
            file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_config["botToken"], file_info.file_path),proxies=bot_config['proxy'])
            botph =bot_config['proxy']
        else:
            file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(bot_config["botToken"], file_info.file_path))
            botph =None
        poh = open("./tmp/"+str(message.from_user.id)+".png",'wb')
        poh.write(file.content)
        poh.close()
        bot.edit_message_text("图片获取完成,上传服务器放大中...", botjson.chat.id, botjson.message_id)
        
        r = requests.post(
            "https://api.deepai.org/api/waifu2x",
            files={
                'image': open("./tmp/"+str(message.from_user.id)+".png", 'rb'),
            },
            headers={'api-key': bot_config['apikey']},proxies=botph
        )
        outjson = r.json()
        file = requests.get(outjson["output_url"],proxies=botph)
        poh = open("./tmp/big"+str(message.from_user.id)+".png",'wb')
        poh.write(file.content)
        poh.close()
        bot.edit_message_text("图片放大完成，正在上传...", botjson.chat.id, botjson.message_id)
        #bot.send_photo(message,outjson["output_url"])
        #bot.reply_to(message,outjson["output_url"])
        photo = open("./tmp/big"+str(message.from_user.id)+".png", 'rb')
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, photo,reply_to_message_id=message.message_id)
        photo.close()
        file_obj=open("./tmp/big"+str(message.from_user.id)+".png",'rb')
        file={'smfile':file_obj}	#参数名称必须为smfile
        data_result=requests.post('https://sm.ms/api/v2/upload',data=None,files=file)
        file_obj.close()
        uplaod = data_result.json()
        if uplaod['success'] == True:
            bot.edit_message_text("上传成功!\n图片地址:"+uplaod['data']['url'], botjson.chat.id, botjson.message_id)
        else:
            bot.edit_message_text("上传成功!\n图片地址: 上传失败", botjson.chat.id, botjson.message_id)
        
        os.remove("./tmp/big"+str(message.from_user.id)+".png")
        os.remove("./tmp/"+str(message.from_user.id)+".png")
    except Exception as oooo:
        bot.send_chat_action(message.chat.id, 'typing')
        #bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
        chatjson_img = bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(oooo))
        time.sleep(3)
        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['gunetmu'])
def gudlwyy(message):
    if howpingip(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /gunetease [网易云音乐ID/网易云分享链接])")
    else:
        try:
            text_rl = howpingip(message.text)
            bot.send_chat_action(message.chat.id, 'typing')
            if is_163pc_url(text_rl) == True:
                chatjson_img = bot.reply_to(message,"识别到网易云网页端的链接...开始解析")
                outnb = urllib.parse.urlparse(text_rl)
                out_quer =outnb.query
                zzout = re.match(r'(id=)[0-9]*',out_quer).group()
                text_ok_id = zzout[3:]
                time.sleep(1)
            elif is_163ph_url(text_rl) == True:
                chatjson_img = bot.reply_to(message,"识别到网易云手机端的链接...开始解析")
                outnb = urllib.parse.urlparse(text_rl)
                out_quer =outnb.query
                zzout = re.match(r'(id=)[0-9]*',out_quer).group()
                text_ok_id = zzout[3:]
                time.sleep(1)
            else:
                try:
                    int(text_rl)
                    chatjson_img = bot.reply_to(message,"识别到网易云音乐ID...开始解析")
                    text_ok_id = text_rl
                    time.sleep(1)
                except:
                    bot.reply_to(message,"抱歉,无法识别"+str(text_rl))
                    return None

            chatjson_img = bot.edit_message_text("解析成功...开始从API获取音乐",chatjson_img.chat.id, chatjson_img.message_id)
            info_musi_info = dl_netmusic_info(text_ok_id)
            chatjson_img = bot.edit_message_text("正在下载『"+info_musi_info['muname']+' - '+info_musi_info['art']+"』请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
            info_music = dl_netmusic(text_ok_id)
            if info_music['success'] == "err":
                 chatjson_img = bot.edit_message_text("抱歉,咕小酱下载音乐时候遇到了未知错误,请重新尝试....",chatjson_img.chat.id, chatjson_img.message_id)
                 return None
            chatjson_img = bot.edit_message_text("正在上传『"+info_musi_info['muname']+' - '+info_musi_info['art']+"』请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
            bot.send_chat_action(message.chat.id, 'upload_audio')
            audio = open(info_music['fil'], 'rb')
            bot.send_audio(message.chat.id, audio,performer=info_music['art'],title=info_music['muname'],reply_to_message_id=message.message_id)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text("『"+info_music['muname']+' - '+info_music['art']+'』上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
            audio.close()
            os.remove(info_music['fil'])
        except Exception as boterr:
            #print(boterr)
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

@bot.message_handler(commands=['gutest'])
def gugugutest(message):
    markup = types.InlineKeyboardMarkup()
    for i in range(0,1):
        btn1 = types.InlineKeyboardButton('咕咕咕'+str(i), callback_data=str(i))
        markup.add(btn1)
    bot.reply_to(message,"这是一个测试",reply_markup=markup)
    print(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handle(call):
    bot.answer_callback_query(call.id, "你点击了第 "+str(call.data)+" 按钮")
    #if call.data == "test":
        #bot.answer_callback_query(call.id, '点我干嘛?')

@bot.message_handler(commands=['gunetsc'])
def guscwyy(message):
    if howpingip(message.text) == False:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,"呜呜呜...指令有问题\n(指令格式 /gunetease [网易云音乐ID/网易云分享链接])")
    else:
        
if __name__ == '__main__':
    while True:
        try:
            logger.info(f"启动成功!")
            bot.polling()
        except Exception as err:
            logger.error(f"遇到错误正在重启:"+str(err))
        time.sleep(1)