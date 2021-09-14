# -*- coding:utf-8 -*-

from telebot import types
from PIL import ImageGrab
from MyEncoder import MyEncoder
from telebot import apihelper
import win32gui, win32ui, win32con
from ctypes import windll
from PIL import ImageFont, ImageDraw, Image
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
from ping3 import ping
import platform
import requests
import numpy as np
import pyautogui
import cv2
import telebot
import json
import os
import time
import yaml
import random
import os.path
import glob


try:

    apihelper.proxy = {'https':'socks5://127.0.0.1:8089'}

    def osu_user_outimg(id): #获取osu用户json信息
        try:
            proxies = {
                'http': 'socks5://127.0.0.1:8089',
                'https': 'socks5://127.0.0.1:8089'
            }


            with open('bot.yaml', 'r') as f: #读取配置文件?
                bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
                token = bottok['osuToken']

            url="https://osu.ppy.sh/api/get_user?k="+token+"&u="+str(id)
            

            res = requests.get(url, proxies=proxies)

            uesr_text = json.loads(res.text)

            ok_userjson = eval(json.dumps(uesr_text[0]))

            down_url = "https://a.ppy.sh/"+ str(ok_userjson['user_id']) +"?img.jpeg" #下载地址合成

            down_res = requests.get(url=down_url,proxies=proxies)

            with open('./tmp/osu/'+str(ok_userjson['user_id'])+'.png',"wb") as code:
                code.write(down_res.content)

            im=Image.open('./osu/img/info.png')
            im1=Image.open('./tmp/osu/'+str(ok_userjson['user_id'])+'.png')
            #im1.thumbnail((700,400))
            im.paste(im1,(279,184))
            im.save('./tmp/osu/'+str(ok_userjson['user_id'])+'ok'+'.png')

            bk_img = cv2.imread('./tmp/osu/'+str(ok_userjson['user_id'])+'ok'+'.png')
            #设置需要显示的字体
            fontpath = "./font/hyl.ttf"
            font = ImageFont.truetype(fontpath, 40)
            img_pil = Image.fromarray(bk_img)
            draw = ImageDraw.Draw(img_pil)
            #绘制文字信息
            draw.text((262, 510),  str(ok_userjson['username']), font = font, fill = (255, 255, 255)) #名字
            draw.text((218, 601),  str(ok_userjson['level']), font = font, fill = (255, 255, 255)) #等级
            draw.text((196, 675),  str(ok_userjson['pp_raw']), font = font, fill = (255, 255, 255)) #PP
            bk_img = np.array(img_pil)


            cv2.imwrite('./tmp/osu/'+str(ok_userjson['user_id'])+'.png',bk_img)
            os.remove('./tmp/osu/'+str(ok_userjson['user_id'])+'ok'+'.png')
            return ok_userjson['user_id']
        except Exception as errr:
            print(errr)
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
        """
        获取节点的延迟的作用
        :param node:
        :return:
        """
        ip_address = ip
        response = ping(ip_address)
        print(response)
        if response is not None:
            delay = response * 1000
            return round(delay,3)
            
        # 下面两行新增的

    def howpingip(textlt): #ping指令识别
        textcomm = textlt
        char_1=' '
        commkgkg=textcomm.find(char_1)
        outip = textcomm[commkgkg+1:len(textcomm)]
        return outip

    def jt_img(idimg):
        img = pyautogui.screenshot(region=[0,0,1920,1080]) # x,y,w,h
        img.save('./tmp/'+str(idimg)+'.png')

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

    def jrrp_text(nub):
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


    with open('bot.yaml', 'r') as f: #读取配置文件?
        bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
        token = bottok['botToken']

    

    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['jrrp'])
    def send_jrrp(message):
        try:
            if fill_json(message.from_user.id) == False:
                #print('创建用户储存文件')
                file = open('./user/jrrp/'+str(message.from_user.id)+'.json','w')
                jrrpp = random.randint(0,100)
                data1 = {
                'jrrp' : jrrpp,
                'time' : time.strftime("%d", time.localtime())
                        }
                file.write(json.dumps(data1))
                file.close()
                bot.reply_to(message, "你今天的人品是："+str(jrrpp)+'\n'+jrrp_text(jrrpp))
            else:
                with open('./user/jrrp/'+str(message.from_user.id)+'.json', 'r') as timejrrp:
                    bottok = eval(json.loads(json.dumps(str(timejrrp.read()))))
                    if time.strftime("%d", time.localtime()) == bottok['time']:
                        bot.reply_to(message, "你今天的人品是："+str(bottok['jrrp'])+'\n'+jrrp_text(bottok['jrrp']))
                    else:
                        file = open('./user/jrrp/'+str(message.from_user.id)+'.json','w')
                        jrrpp = random.randint(0,100)
                        data1 = {
                            'jrrp' : jrrpp,
                            'time' : time.strftime("%d", time.localtime())
                                }
                        file.write(json.dumps(data1))
                        file.close()
                        bot.reply_to(message, "你今天的人品是："+str(jrrpp)+'\n'+jrrp_text(jrrpp))
        except Exception as errr:
            bot.reply_to(message, '呜呜呜....程序出错了惹\n错误日志: '+str(errr))

    @bot.message_handler(commands=['gu'])
    def send_gu(message):
        try:
            if random.randint(0,10) >= 5:
                bot.reply_to(message, mult_times('咕', 1, random.randint(0,10)))
            else:
                path_file_name=glob.glob(pathname='./img/*.webp') #获取当前文件夹下个数
                sti = open(path_file_name[random.randint(0,len(path_file_name)-1)], 'rb')
                bot.send_sticker(message.chat.id, sti)
        except Exception as errr:
            bot.reply_to(message, '呜呜呜....图片没上传及时.......\n错误日志: '+str(errr))
        
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
            bot.reply_to(message, '你获得一只:'+ what_phi(guuu)+'\n-好感度: 100\n-饱食度: 100\n-饥渴度: 0')
        else:
            bot.reply_to(message,"你已经领养了一只小鸽子(")

    @bot.message_handler(commands=['killpigeons'])
    def send_kill(message): #kill
        if ycxt_json(message.from_user.id) == False:
            bot.reply_to(message,"你还没领养小鸽子(")
        else:
            os.remove('./user/ycxt/'+str(message.from_user.id)+'.json')
            bot.reply_to(message,"小鸽子被你炖了吃了....")

    @bot.message_handler(commands=['gugugu'])
    def send_aaa(message): #互动
        if ycxt_json(message.from_user.id) == False:
            bot.reply_to(message,"你还没领养小鸽子(")
        else:
            bot.reply_to(message,"代码先咕咕咕了")

    @bot.message_handler(commands=['gubaidu'])
    def send_baidu(message):
        bot.reply_to(message,'功能已下线')
        #bot.reply_to(message,baidurs())

    @bot.message_handler(commands=['guweibo'])
    def send_weibo(message):
        bot.reply_to(message,'微博热搜:\n'+weibo_hot())

    @bot.message_handler(commands=['lookgu'])
    def send_jtimg(message):
        if message.from_user.id == 1431873495:
            jt_img(message.from_user.id)
            photo = open('./tmp/'+str(message.from_user.id)+'.png', 'rb')
            bot.send_photo(message.chat.id, photo)
            time.sleep(5)
            #os.remove('./tmp/'+str(message.from_user.id)+'.png')
        else:
            bot.reply_to(message,'想什么呢你没权限(')

    @bot.message_handler(commands=['guping'])
    def send_jtimg(message):
        try:
            if yesnocoom(message.text) == True:
                pingipp = howpingip(message.text)
                chatjson = bot.reply_to(message,'正在执行Ping '+str(pingipp))
                if str(ping_host(str(pingipp))) == 'None':
                    bot.edit_message_text('咕小酱Ping不通....呜呜呜\n', chatjson.chat.id, chatjson.message_id)
                else:
                    bot.edit_message_text(str(pingipp)+' 的延迟为: \n\n'+str(ping_host(str(pingipp))) + ' ms', chatjson.chat.id, chatjson.message_id)
                #print(output_str)
            else:
                bot.reply_to(message,'想什么呢?\n你指令有问题.....')
        except Exception as pingerr:
            bot.reply_to(message, '呜呜呜....执行Ping指令时出错了\n错误日志: '+str(pingerr))

    @bot.message_handler(commands=['guosu'])
    def guosu(message):
        try:
            chatjson_img = bot.reply_to(message,"正在生成图片请稍后....")
            out = osu_user_outimg(howpingip(message.text))
            if osu_user_outimg(howpingip(message.text)) == False:
                pass
            else:
                chatjson_img = bot.edit_message_text("正在上传图片请稍后....",chatjson_img.chat.id, chatjson_img.message_id)
                phpget = open('./tmp/osu/'+str(out)+'.png','rb')
                bot.send_photo(message.chat.id, phpget)
        except Exception as boterr:
            bot.reply_to(message, '呜呜呜...指令有问题......\n错误日志: '+str(boterr))

    if __name__ == '__main__':
        bot.polling()

except Exception as boterr:
    print(boterr)
    bot.polling()