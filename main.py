# -*- coding:utf-8 -*-
from telebot import apihelper
from bs4 import BeautifulSoup
from lxml import etree
from decimal import Decimal
from ping3 import ping
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
import cairosvg

#初始化
def oneload():
    if os.path.exists("./config.yml") == False:
        print("未检测到配置文件\n开始初始化")
        with open("./config.yml", 'wb') as f:
            f.write(bytes("botToken: \nosuToken: \nproxybool: False\nproxy: {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'}",'utf-8'))
            f.close()
        print("开始创建文件夹")
        os.mkdir("./dl-tmp")
        os.mkdir("./img")
        os.mkdir("./osu")
        os.mkdir("./tmp")
        os.mkdir("./tmp/osu")
        os.mkdir("./user")
        os.mkdir("./user/jrrp")
        os.mkdir("./user/ycxt")
        print("文件夹创建完毕")
        print("开始下载表情包")
        r =  requests.get("https://cdn.jsdelivr.net/gh/GooguJiang/gu_img/img.zip")
        with open("./dl-tmp/img.zip",'wb') as code:
            code.write(r.content)
        print('表情包下载完成')
        print("开始解压文件")
        zip_file = zipfile.ZipFile("./dl-tmp/img.zip")
        zip_list = zip_file.namelist() 
        for f in zip_list: 
            zip_file.extract(f,"./")
        zip_file.close() 
        print("文件解压完毕")
        print("删除缓存")
        os.remove("./dl-tmp/img.zip")
        print("初始化完毕请填写配置文件然后重新运行本程序!")
        sys.exit()
    else:
        print("加载配置文件")

oneload()

try:
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

    def dl_sdmusic_info(url_dl):
        try:
            with open('config.yml', 'r') as f: #读取配置文件?
                    bottok = yaml.load(f.read(),Loader=yaml.FullLoader)

            # post参数合成区
            url = 'https://soundcloudmp3.cc/ajax.php'

            proxies = bottok['proxy']

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            }


            data =  {"action": "video_preview","vidURL": url_dl,"tType":"trim" }
            # post访问
            if bottok['proxybool'] == True:
                response = requests.post(url=url, headers=headers, data=data,proxies=proxies)
            else:
                response = requests.post(url=url, headers=headers, data=data)
            page_text = json.loads(str(response.text))
            return page_text["vidTitle"]
        except Exception as ooo:
            print(ooo)
            return False

    def getStrAsMD5(parmStr):
        if isinstance(parmStr,str):
            parmStr = parmStr.encode("utf-8")
        m = hashlib.md5()
        m.update(parmStr)
        return m.hexdigest()

    def dl_sdmusic(url_dl):
        try:
            with open('config.yml', 'r') as f: #读取配置文件?
                    bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
            # post参数合成区
            url = 'https://soundcloudmp3.cc/ajax.php'

            proxies = bottok['proxy']

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            }


            data =  {"action": "video_preview","vidURL": url_dl,"tType":"trim" }


            # post访问
            if bottok['proxybool'] == True:
                response = requests.post(url=url, headers=headers, data=data,proxies=proxies)
            else:
                response = requests.post(url=url, headers=headers, data=data)
            page_text = json.loads(str(response.text))
            down_url = "https://soundcloudmp3.cc/"+page_text["vidSrc"][1:]
            if bottok['proxybool'] == True:
                res = requests.get(down_url,proxies=proxies)
            else:
                res = requests.get(down_url)
            
            try:
                with open("./dl-tmp/"+page_text["vidTitle"]+'.mp3', 'wb') as f:
                    f.write(res.content)
            except:
                with open("./dl-tmp/"+getStrAsMD5(page_text["vidTitle"])+'.mp3', 'wb') as f:
                    f.write(res.content)
            #下载专辑图片
            dl_img = repr(page_text["vidImage"])
            dl_img = dl_img[1:len(dl_img)-1]
            if bottok['proxybool'] == True:
                res = requests.get(dl_img,proxies=proxies)
            else:
                res = requests.get(dl_img)
            
            try:
                with open("./dl-tmp/"+page_text["vidTitle"]+'.jpg', 'wb') as f:
                    f.write(res.content)
            except:
                with open("./dl-tmp/"+getStrAsMD5(page_text["vidTitle"])+'.jpg', 'wb') as f:
                    f.write(res.content)

            #写入信息
            try:
                audiofile = eyed3.load("./dl-tmp/"+page_text["vidTitle"]+'.mp3')  # 读取mp3文件
                audiofile.initTag()  # 初始化所有标签信息，将之前所有的标签清除
                audiofile.tag.images.set(3, open("./dl-tmp/"+page_text["vidTitle"]+'.jpg','rb').read(), 'image/jpeg') #添加封面
                audiofile.tag.album = u"SoundCloud"  # 唱片集
                audiofile.tag.title = page_text["vidTitle"]  # 标题
                audiofile.tag.save() # 保存文件
                os.remove("./dl-tmp/"+page_text["vidTitle"]+'.jpg')
                fill = page_text["vidTitle"]
            except:
                audiofile = eyed3.load("./dl-tmp/"+getStrAsMD5(page_text["vidTitle"])+'.mp3')
                audiofile.initTag()  # 初始化所有标签信息，将之前所有的标签清除
                audiofile.tag.images.set(3, open("./dl-tmp/"+getStrAsMD5(page_text["vidTitle"])+'.jpg','rb').read(), 'image/jpeg') #添加封面
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

    def new_gosu(name): # OSU模式
        try:
            with open('config.yml', 'r') as f: #读取配置文件?
                    bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
                    token = bottok['osuToken']

            url="https://osu.ppy.sh/api/get_user?k="+token+"&u="+str(name)
            if bottok['proxybool'] == True:
                proxies = bottok['proxy']
                res = requests.get(url, proxies=proxies)
            else:
                res = requests.get(url)
                
            uesr_text = json.loads(res.text) #json解析
            ok_userjson = eval(json.dumps(uesr_text[0]))
            #print(ok_userjson)    
            down_url = "https://osu-stats-signature.vercel.app/card?user="+ str(ok_userjson['user_id']) +"&mode=std&blur=6&w=1920&h=1117" #下载地址合成
            if bottok['proxybool'] == True:
                proxies = bottok['proxy']
                down_res = requests.get(url=down_url,proxies=proxies)
            else:
                down_res = requests.get(url=down_url)
            
            with open('./tmp/osu/'+str(ok_userjson['user_id'])+'.svg',"wb") as code:
                code.write(down_res.content)
            cairosvg.svg2png(url='./tmp/osu/'+str(ok_userjson['user_id'])+'.svg', write_to='./tmp/osu/'+str(ok_userjson['user_id'])+'.png')
            os.remove('./tmp/osu/'+str(ok_userjson['user_id'])+'.svg')
            return ok_userjson['user_id']
        except Exception as errr:
            print(errr)
            return False

    with open('config.yml', 'r') as f: #读取配置文件?
            botproxy = yaml.load(f.read(),Loader=yaml.FullLoader)
            botproxyyesno = botproxy['proxybool']

    if botproxyyesno == True:
        apihelper.proxy = botproxy['proxy']


    def num_out(in1,in2): #减法
        if str(in1) == str(in2):
            return False
        else:
            return round(Decimal(in1),4) - round(Decimal(in2),4)

    def PP(index_array,text_array): #百度排序
        x = {}
        i = 0
        for index_a in index_array:
            #index_a = int(index_a)
            
            x[index_a] = text_array[i]
            i = i + 1
        return x


    def get_osuid(name):
        try:


            with open('config.yml', 'r') as f: #读取配置文件?
                bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
                token = bottok['osuToken']
            proxies = bottok['proxy']
            
            url="https://osu.ppy.sh/api/get_user?k="+token+"&u="+str(name)
            if bottok['proxybool'] == True:
                proxies = bottok['proxy'] 
                res = requests.get(url, proxies=proxies)
            else:
                res = requests.get(url)

            uesr_text = json.loads(res.text)

            ok_userjson = eval(json.dumps(uesr_text[0]))

            return ok_userjson
        except:
            return False

    def get_random():

        with open('config.yml', 'r') as f: #读取配置文件?
            bottok = yaml.load(f.read(),Loader=yaml.FullLoader)

        url='https://www.random.org/integers/?num=1&min=0&max=100&col=1&base=10&format=plain&rnd=new'

        proxies = bottok['proxy']

        if bottok['proxybool'] == True:
            res = requests.get(url, proxies=proxies)
        else:
            res = requests.get(url)


        return res.text


    def osu_user_outinfo(id,mode): #TG绑定信息查询专用
        try:

            with open('config.yml', 'r') as f: #读取配置文件?
                bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
                token = bottok['osuToken']

            url="https://osu.ppy.sh/api/get_user?k="+token+"&u="+str(id)
            if bottok['proxybool'] == True:
                proxies = bottok['proxy']
                res = requests.get(url, proxies=proxies)
            else:
                res = requests.get(url)
            uesr_text = json.loads(res.text) #json解析
            ok_userjson = eval(json.dumps(uesr_text[0]))

            osu_now_level = ok_userjson['level']
            osu_now_pp = ok_userjson['pp_raw']

            osu_out_level = num_out(osu_now_level,out_osuinfo(id,4)) #等级差计算
            if osu_out_level == False:
                osu_level_out = '-'
            elif osu_out_level >0:
                osu_level_out = str(osu_out_level)+'↑'
            else:
                osu_level_out = str(osu_out_level)+'↓'
            
            osu_out_pp = num_out(osu_now_pp,out_osuinfo(id,5)) #PP差计算
            if osu_out_pp == False:
                osu_pp_out = '-'
            elif osu_out_pp >0:
                osu_pp_out = str(osu_out_pp)+'↑'
            else:
                osu_pp_out = str(osu_out_pp)+'↓'

            #------------------------
            tg_sql_id = out_osuinfo(id,0)
            osu = sqlite3.connect("./osu/osu.db")
            cur = osu.cursor()
            cur.execute("DELETE FROM osuinfo WHERE telid=?", (tg_sql_id,))
            osu.commit()
            # 关闭游标
            cur.close()
            # 断开数据库连接
            osu.close()
            inpu_osuinfo(tg_sql_id,id,osu_now_level,osu_now_pp)
            #------------------------

            down_url = "https://osu-stats-signature.vercel.app/card?user="+ str(ok_userjson['user_id']) +"&mode="+str(mode)+"&blur=6&w=1920&h=1117" #下载地址合成
            if bottok['proxybool'] == True:
                proxies = bottok['proxy']
                down_res = requests.get(url=down_url,proxies=proxies)
            else:
                down_res = requests.get(url=down_url)
            
            with open('./tmp/osu/'+str(ok_userjson['user_id'])+'.svg',"wb") as code:
                code.write(down_res.content)
            cairosvg.svg2png(url='./tmp/osu/'+str(ok_userjson['user_id'])+'.svg', write_to='./tmp/osu/'+str(ok_userjson['user_id'])+'.png')
            os.remove('./tmp/osu/'+str(ok_userjson['user_id'])+'.svg')

            return ok_userjson['user_id']
        except Exception as errr:
            print(errr)
            return False

    def inpu_osuinfo(teleid,userosuid,level,pp): #数据文件写入
        try:
            osu = sqlite3.connect("./osu/osu.db")
            cur = osu.cursor()
            sql = "CREATE TABLE IF NOT EXISTS osuinfo(telid INTEGER PRIMARY KEY,osuid INTEGER,level INTEGER,pp INTEGER)"
            cur.execute(sql)
            cur.execute("INSERT INTO osuinfo values(?,?,?,?)", (teleid, userosuid,level,pp))
            osu.commit()
            # 关闭游标
            cur.close()
            # 断开数据库连接
            osu.close()
            return True
        except Exception as ree:
            print('数据库处理出错!\n错误日志: '+str(ree))
            cur.close()
            # 断开数据库连接
            osu.close()
            return False

    def out_osuinfo(teleid,oid):
        osu = sqlite3.connect("./osu/osu.db")
        cur = osu.cursor()
        sql = "CREATE TABLE IF NOT EXISTS osuinfo(telid INTEGER PRIMARY KEY,osuid INTEGER,level INTEGER,pp INTEGER)"
        cur.execute(sql)
        osu.commit()
        cur.execute("select * from osuinfo")
        sence = cur.fetchall()
        if oid == 1:
            for i in range(len(sence)): #TG取OSU ID
                #print(sence[i][0])
                if str(sence[i][0]) == teleid:
                    return sence[i][1]
        elif oid == 0:
            for i in range(len(sence)): # OSU ID取 TG
                #print(sence[i][0])
                if str(sence[i][1]) == teleid:
                    return sence[i][0]                                             #写的头疼（
        elif oid == 2:
            for i in range(len(sence)): #OSU ID取OSU ID
                #print(sence[i][0])
                if str(sence[i][1]) == teleid:
                    return sence[i][1]
        elif oid == 3:
            for i in range(len(sence)): #TG取TG
                #print(sence[i][0])
                if str(sence[i][0]) == teleid:
                    return sence[i][0]
        elif oid == 4:
            for i in range(len(sence)): #TG取OSU 等级
                #print(sence[i][0])
                if str(sence[i][1]) == teleid:
                    return sence[i][2]
        elif oid == 5:
            for i in range(len(sence)): #TG取 PP
                #print(sence[i][0])
                if str(sence[i][1]) == teleid:
                    return sence[i][3]
        else:
            return False


    def yesnocoom(incom): #检测ping指令是否正确
        str_1=incom
        char_1=str(' ')
        count=0
        str_list=list(str_1)
        how_text = []
        for each_char in str_list:
            count+=1
            if each_char==char_1:          
                out_hoow = count-1
                how_text.append(str(out_hoow))
        if len(how_text) == 1:
            return True
        else:
            return False
    
    def ping_host(ip):
        ip_address = ip
        response = ping(ip_address)
        #print(response)
        if response is not None:
            delay = response * 1000
            return round(delay,3)
            
        # 下面两行新增的

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
        

    def weibo_hot():
        news = []
        # 新建数组存放热搜榜
        hot_url = 'https://s.weibo.com/top/summary/'
        # 热搜榜链接
        r = requests.get(hot_url)
        # 向链接发送get请求获得页面
        soup = BeautifulSoup(r.text, 'lxml')
        # 解析页面

        urls_titles = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > a')
        hotness = soup.select('#pl_top_realtimehot > table > tbody > tr > td.td-02 > span')

        for i in range(10):
            hot_news = ''
            # 将信息保存到字典中
            hot_news = str(i+1) + '.' + urls_titles[i+1].get_text() + '|热度：'+hotness[i].get_text()

            news.append(hot_news) 
            # 字典追加到数组中 
        return news[0]+'\n'+news[1]+'\n'+news[2]+'\n'+news[3]+'\n'+news[4]+'\n'+news[5]+'\n'+news[6]+'\n'+news[7]+'\n'+news[8]+'\n'+news[9]


    def get_phi():
        return random.randint(0,4)

    def what_phi(id):
        gugu = ['野鸽','雪鸽','迷鸽','信鸽','雀鸽']
        return gugu[id]

    def mult_times(str, m, n): #指定次数
        front_len = m
        if front_len > len(str):
            front_len = len(str)
        front = str[:front_len]

        result = ''
        for i in range(n):
            result = result + front
        return result

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

    def ycxt_json(id): #让我康康你领取鸽子了吗?
        if os.path.isfile('./user/ycxt/'+str(id)+'.json') == True:
            return True
        else:
            return False


    with open('config.yml', 'r') as f: #读取配置文件?
        bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
        token = bottok['botToken']

#----------------------👆函数区👆-------------------------------   

    bot = telebot.TeleBot(token)

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
            bot.reply_to(message, '呜呜呜....程序出错了惹\n错误日志: '+str(errr))

    @bot.message_handler(commands=['gu'])
    def send_gu(message):
        try:
            if random.randint(0,10) >= 5:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message, mult_times('咕', 1, random.randint(0,10)))
            else:
                path_file_name=glob.glob(pathname='./img/*.webp') #获取当前文件夹下个数
                sti = open(path_file_name[random.randint(0,len(path_file_name)-1)], 'rb')
                bot.send_chat_action(message.chat.id, 'upload_photo')
                bot.send_sticker(message.chat.id, sti)
        except Exception as errr:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, '呜呜呜....图片没上传及时.......')
        
    @bot.message_handler(commands=['getpigeons'])
    def send_feed(message): #领养鸽子
        if ycxt_json(message.from_user.id) == False:
            #print(ycxt_json(message.from_user.id))
            file = open('./user/ycxt/'+str(message.from_user.id)+'.json','w',encoding='utf-8')
            guuu = get_phi()
            data_gu = {
            'impress' : 100,
            'food' : 100,
            'water': 100,
            'variety': guuu
                    }
            file.write(json.dumps(data_gu))
            file.close()
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, '你获得一只:'+ what_phi(guuu)+'\n-好感度: 100\n-饱食度: 100\n-饥渴度: 0')
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"你已经领养了一只小鸽子(")

    @bot.message_handler(commands=['killpigeons'])
    def send_kill(message): #kill
        if ycxt_json(message.from_user.id) == False:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"你还没领养小鸽子(")
        else:
            os.remove('./user/ycxt/'+str(message.from_user.id)+'.json')
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"小鸽子被你炖了吃了....")

    @bot.message_handler(commands=['gugugu'])
    def send_aaa(message): #互动
        if ycxt_json(message.from_user.id) == False:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"你还没领养小鸽子(")
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"代码先咕咕咕了")

    @bot.message_handler(commands=['gubaidu'])
    def send_baidu(message):
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
            page = requests.get("https://www.baidu.com",headers=headers)
            html = page.text
            #print(source1)
            # 从字符串解析
            element = etree.HTML(html)

            # 元素列表，获取的方式列出了如下两种
            # ps = element.xpath('//*[@id="hotsearch-content-wrapper"]/li/a/span[2]')
            ps = element.xpath('//*[@class="title-content-title"]')

            #热搜文本内容
            text = []
            if len(ps) > 0:
                for p in ps:
                    #输出节点的文本
                    text1 = p.text
                    text.append(text1)
            else:
                print("空")
                
            x = element.xpath('//*[@class="s-hotsearch-content"]/li')

            #热搜文本对应的排名
            index = []
            for x1 in x:
                #获取节点的属性
                index1 = x1.get("data-index")
                index.append(index1)
            re_text = PP(index,text)
            #对字典性数据按key进行排序，即key=lambda re:re[0]，排序完成后再转换为字典型数据
            last_text = dict(sorted(re_text.items(),key=lambda re:re[0]))
            baidu_text  = '百度热搜:\n'
            for nu in range(1,6):
                baidu_text += str(nu)+'.'+str(last_text[str(nu)])+'\n'
            bot.reply_to(message,baidu_text)
        except Exception as xxxx:
            bot.reply_to(message,xxxx)

    @bot.message_handler(commands=['guweibo'])
    def send_weibo(message):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message,'微博热搜:\n'+weibo_hot())


    @bot.message_handler(commands=['guping'])
    def send_jtimg(message):
        try:
            if howpingip(message.text) == False:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"呜呜呜....你光发个指令干嘛让我Ping寂寞啊~\n(缺少参数/guping [Ping的地址])")
            else:
                if yesnocoom(message.text) == True:
                    pingipp = howpingip(message.text)
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson = bot.reply_to(message,'正在执行Ping '+str(pingipp))
                    if str(ping_host(str(pingipp))) == 'None':
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('咕小酱Ping不通....呜呜呜\n', chatjson.chat.id, chatjson.message_id)
                    else:
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text(str(pingipp)+' 的延迟为: \n\n'+str(ping_host(str(pingipp))) + ' ms', chatjson.chat.id, chatjson.message_id)
                    #print(output_str)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,'想什么呢?\n你指令有问题.....')
        except Exception as pingerr:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message, '呜呜呜....执行Ping指令时出错了\n错误日志: '+str(pingerr))

    @bot.message_handler(commands=['guosu'])
    def guosu(message):
        try:
            
            if howpingip(message.text) == False:
                if out_osuinfo(str(message.from_user.id),3) == None:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,"你指令不保熟啊!\n(缺少参数/guosu [OSU用户名/OSU ID] 或者 /guosubind [OSU用户名/OSU ID] 来绑定)")
                else:
                    try:
                        bot.send_chat_action(message.chat.id, 'typing')
                        chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                        out = osu_user_outinfo(str(out_osuinfo(str(message.from_user.id),1)),"std")
                        chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                        bot.send_chat_action(message.chat.id, 'upload_photo')
                        phpget = open('./tmp/osu/'+str(out)+'.png','rb')
                        bot.send_photo(message.chat.id, phpget)
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                        phpget.close()
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                    except Exception as gubot:
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
            else:
                try:
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                    out = new_gosu(howpingip(message.text))

                    chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)

                    bot.send_chat_action(message.chat.id, 'upload_photo')

                    phpget = open('./tmp/osu/'+str(out)+'.png','rb')

                    bot.send_photo(message.chat.id, phpget)
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                    time.sleep(3)
                    bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                except Exception as gubot:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
        except Exception as boterr:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

    @bot.message_handler(commands=['guosubind'])
    def send_osuinfo(message):
        outtext = howpingip(message.text)
        #print(outtext) #指令输出
        if outtext == False:
            if out_osuinfo(str(message.from_user.id),3) == None:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,"你指令不保熟啊!\n(缺少参数/guosu [OSU用户名/OSU ID] 或者 /guosubind [OSU用户名/OSU ID] 来绑定)")
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,"你已经绑定过 OSU 用户名了,如需更改请发送 /guosudel 重新绑定哦~")
        else:
            try: 
                osuid = get_osuid(outtext)
                if osuid != False:

                        #print(out_osuinfo(message.from_user.id,3)) #数据库检测
                        if out_osuinfo(str(message.from_user.id),3) == None:
                            if out_osuinfo(str(osuid['user_id']),2) == None:
                                bot.send_chat_action(message.chat.id, 'typing')
                                chatjson_sql = bot.reply_to(message,"正在绑定....")
                                if inpu_osuinfo(message.from_user.id,osuid['user_id'],osuid['level'],osuid['pp_raw']) == True:
                                    bot.send_chat_action(message.chat.id, 'typing')
                                    bot.edit_message_text('绑定 OSU 用户名成功啦!',chatjson_sql.chat.id, chatjson_sql.message_id)
                                else:
                                    bot.send_chat_action(message.chat.id, 'typing')
                                    bot.reply_to(message,"此 OSU 用户名不存在或者数据库处理出错的说...")
                            else:
                                bot.send_chat_action(message.chat.id, 'typing')
                                bot.reply_to(message,"此 OSU 用户名已经被其他 Telegram ID 绑定了惹...")
                        else:
                            bot.send_chat_action(message.chat.id, 'typing')
                            bot.reply_to(message,"你的Telegram ID 绑定了 OSU 用户名了的说...")
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,"此 OSU 用户名不存在或者数据库处理出错的说...")

            except Exception as ooo:
                #inpu_osuinfo(message.from_user.id,osuid)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.reply_to(message,'呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(ooo))

    #数据库读取函数后面参数? (自造)
    # #0 OSU ID 取 Telegeam ID
    # #1 Telegeam ID 取 OSU ID 
    # #2 OSU ID 取 OSU ID 
    # #3 Telegram ID取 TG

    
    @bot.message_handler(commands=['guosudel'])
    def send_infopho(message):
        if out_osuinfo(str(message.from_user.id),3) == None:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.reply_to(message,"你的 Telegram ID 未绑定 OSU 用户名\n请使用: \n/guosubind [OSU用户名/OSU ID] \n来绑定吧!")
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            chatjson_del = bot.reply_to(message,"正在解绑 OSU 用户名中....")
            osu = sqlite3.connect("./osu/osu.db")
            cur = osu.cursor()
            cur.execute("DELETE FROM osuinfo WHERE telid=?", (message.from_user.id,))
            osu.commit()
            # 关闭游标
            cur.close()
            # 断开数据库连接
            osu.close()
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('OSU 用户名解绑完成!',chatjson_del.chat.id, chatjson_del.message_id)

    @bot.message_handler(commands=['guzhihu'])
    def send_zhihu(message):
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            zhihu_text_go = bot.reply_to(message,'正在获取请稍后...')
            zhihu_json_input = requests.get("https://tenapi.cn/zhihuresou")
            zhihu_json_out = eval(json.dumps(json.loads(zhihu_json_input.text)))
            zhihu_json_list = zhihu_json_out['list']
            zhihu_text = '知乎热搜:\n'
            for i in range(0, 10):
                zhihu_text += str(i+1)+'.『'+str(zhihu_json_list[i]['name'])+'』 - '+ str(zhihu_json_list[i]['query'])+'\n'
            bot.edit_message_text(zhihu_text,zhihu_text_go.chat.id, zhihu_text_go.message_id)
            #bot.reply_to(message,zhihu_text)
        except:
            bot.edit_message_text('呜呜呜....运行错误',zhihu_text_go.chat.id, zhihu_text_go.message_id)

    @bot.message_handler(commands=['gubili'])
    def send_bilibili(message):
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            bili_json_input = requests.get("https://hibiapi.aliserver.net/api/bilibili/v3/video_ranking")
            if bili_json_input.status_code == 200:
                try:
                    bili_text_go = bot.reply_to(message,'正在获取请稍后...')
                    bili_json_list = json.loads(bili_json_input.content)['rank']['list']
                    #print(bili_json_list)
                except:
                    pass
            #bili_json_out = eval(json.dumps(json.loads(bili_json_input.text)))
            #print(bili_json_out)
            #bili_json_list = bili_json_out['rank']['list']
            bili_text = 'BiliBili热门视频排行榜Top10:\n'
            for i in range(0, 10):
                bili_text += str(i+1)+'.『'+str(bili_json_list[i]['title'])+'』 | UP主:'+ str(bili_json_list[i]['author'])+'\n'
            bot.edit_message_text(bili_text,bili_text_go.chat.id, bili_text_go.message_id)
            #bot.reply_to(message,bili_text)
        except Exception as eeer:
            bot.edit_message_text('呜呜呜....运行错误',bili_text_go.chat.id, bili_text_go.message_id)

    @bot.message_handler(commands=['guosutaiko'])
    def guosutk(message):
        try:
                
            if howpingip(message.text) == False:
                if out_osuinfo(str(message.from_user.id),3) == None:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,"你指令不保熟啊!\n(缺少参数/guosutaiko [OSU用户名/OSU ID] 或者 /guosubind [OSU用户名/OSU ID] 来绑定)")
                else:
                    try:
                        bot.send_chat_action(message.chat.id, 'typing')
                        chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                        out = osu_user_outinfo(str(out_osuinfo(str(message.from_user.id),1)),"taiko")
                        chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                        bot.send_chat_action(message.chat.id, 'upload_photo')
                        phpget = open('./tmp/osu/'+str(out)+'.png','rb')
                        bot.send_photo(message.chat.id, phpget)
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                        phpget.close()
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                    except Exception as gubot:
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
            else:
                try:
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                    out = new_gosu(howpingip(message.text))

                    chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)

                    bot.send_chat_action(message.chat.id, 'upload_photo')

                    phpget = open('./tmp/osu/'+str(out)+'.png','rb')

                    bot.send_photo(message.chat.id, phpget)
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                    phpget.close()
                    time.sleep(3)
                    bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                except Exception as gubot:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
        except Exception as boterr:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

    @bot.message_handler(commands=['guosucatch'])
    def guosuca(message):
        try:
                
            if howpingip(message.text) == False:
                if out_osuinfo(str(message.from_user.id),3) == None:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,"你指令不保熟啊!\n(缺少参数/guosucatch [OSU用户名/OSU ID] 或者 /guosubind [OSU用户名/OSU ID] 来绑定)")
                else:
                    try:
                        bot.send_chat_action(message.chat.id, 'typing')
                        chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                        out = osu_user_outinfo(str(out_osuinfo(str(message.from_user.id),1)),"catch")
                        chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                        bot.send_chat_action(message.chat.id, 'upload_photo')
                        phpget = open('./tmp/osu/'+str(out)+'.png','rb')
                        bot.send_photo(message.chat.id, phpget)
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                        phpget.close()
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                    except Exception as gubot:
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
            else:
                try:
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                    out = new_gosu(howpingip(message.text))

                    chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)

                    bot.send_chat_action(message.chat.id, 'upload_photo')

                    phpget = open('./tmp/osu/'+str(out)+'.png','rb')

                    bot.send_photo(message.chat.id, phpget)
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                    phpget.close()
                    time.sleep(3)
                    bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                except Exception as gubot:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
        except Exception as boterr:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

    @bot.message_handler(commands=['guosumania'])
    def guosuman(message):
        try:
                
            if howpingip(message.text) == False:
                if out_osuinfo(str(message.from_user.id),3) == None:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.reply_to(message,"你指令不保熟啊!\n(缺少参数/guosumania [OSU用户名/OSU ID] 或者 /guosubind [OSU用户名/OSU ID] 来绑定)")
                else:
                    try:
                        bot.send_chat_action(message.chat.id, 'typing')
                        chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                        out = osu_user_outinfo(str(out_osuinfo(str(message.from_user.id),1)),"mania")
                        chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                        bot.send_chat_action(message.chat.id, 'upload_photo')
                        phpget = open('./tmp/osu/'+str(out)+'.png','rb')
                        bot.send_photo(message.chat.id, phpget)
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                        phpget.close()
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                    except Exception as gubot:
                        bot.send_chat_action(message.chat.id, 'typing')
                        bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
                        time.sleep(3)
                        bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
            else:
                try:
                    bot.send_chat_action(message.chat.id, 'typing')
                    chatjson_img = bot.reply_to(message,"正在查询生成图片请稍后....")
                    out = new_gosu(howpingip(message.text))
                    chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                    bot.send_chat_action(message.chat.id, 'upload_photo')
                    phpget = open('./tmp/osu/'+str(out)+'.png','rb')
                    bot.send_photo(message.chat.id, phpget)
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('图片上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                    phpget.close()
                    time.sleep(3)
                    bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                except Exception as gubot:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text('上传时出错了惹...\n错误日志: '+str(gubot),chatjson_img.chat.id, chatjson_img.message_id)
        except Exception as boterr:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
            time.sleep(3)
            bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

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
                    audio = open("./dl-tmp/"+dl_muss+".mp3", 'rb')
                    bot.send_audio(message.chat.id, audio)
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.edit_message_text("『"+info_music+'』上传完成!', chatjson_img.chat.id, chatjson_img.message_id)
                    time.sleep(3)
                    bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)
                    audio.close()
                    os.remove("./dl-tmp/"+dl_muss+".mp3")
            except Exception as boterr:
                #print(boterr)
                bot.send_chat_action(message.chat.id, 'typing')
                bot.edit_message_text('呜呜呜...咕小酱遇到了严重问题......\n错误日志: '+str(boterr),chatjson_img.chat.id, chatjson_img.message_id)
                time.sleep(3)
                bot.delete_message(chatjson_img.chat.id, chatjson_img.message_id)

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
            bot.edit_message_text('呜呜呜....运行错误',hhsh_text_go.chat.id, hhsh_text_go.message_id)

    if __name__ == '__main__':
        bot.polling()

except Exception as boterr:
    while True:
        print("程序出错正在重启"+str(boterr))
        bot.polling()
        time.sleep(10)