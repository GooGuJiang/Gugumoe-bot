from icmplib import traceroute
from icmplib import ping
from qqwry import QQwry
import socket
import re
from PIL import Image, ImageFont, ImageDraw

czip = QQwry()
czip.load_file('./ip_data/qqwry.dat')

def yes_or_no_ip(str):
    try:
        pattern = re.compile(r'^((2(5[0-5]|[0-4]\d))|1\d{2}|[1-9]?\d)(\.((2(5[0-5]|[0-4]\d))|1\d{2}|[1-9]?\d)){3}$')
        test = pattern.search(str)
        if str == test.group():
            return True
        else:
            return False
    except:
        return False

def yes_or_no_ip6(str):
    try:
        ip6_regex = (
                r'(^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$)|'
                r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,6}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|'
                r'(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4}){1,7}\Z)|'
                r'(\A((([0-9a-f]{1,4}:){6})(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
                r'(\A(([0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
                r'(\A([0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,4}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,3}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,2}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,1}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                r'(\A(([0-9a-f]{1,4}:){1,5}|:):(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                r'(\A:(:[0-9a-f]{1,4}){1,5}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)')
        pattern = re.compile(ip6_regex)
        test = pattern.search(str)
        #print(test)
        if str == test.group():
            return True
        else:
            return False
    except:
        return False

def gu_traceroute(ip): # ip路由
    try:
        gu_tmp = ""
        hops = traceroute(str(ip),count=1,fast=True,timeout=0.8)
        last_distance = 0
        for hop in hops:
            if last_distance + 1 != hop.distance:
                gu_tmp += f'{hop.distance} | {hop.address} {czip.lookup(hop.address)[0]}({czip.lookup(hop.address)[1]})  {hop.avg_rtt} ms\n'
                last_distance = hop.distance
        return gu_tmp.strip('\n')
    except:
        return False

def gu_ping(ip):# ping 测试
    try:
        gu_tmp = ""
        hops = ping(str(ip), count=4, interval=0.2)
        for nub in range(len(hops.rtts)):
            gu_tmp += f"{nub+1} | {hops.address}  {round(hops.rtts[nub],2)} ms\n"
        gu_tmp += f"平均延迟 {hops.avg_rtt} ms"
        if len(hops.rtts) == 0:
            return False
        return gu_tmp
    except:
        return False

def get_utlurls(html):
    pattren = re.compile(r'http://')
    url_lst = pattren.findall(html)
    if len(url_lst) == 0:
        pattren = re.compile(r'https://')
        url_lst = pattren.findall(html)
        if len(url_lst) == 0:
            return False
        else:
            return html[8:len(html)]
    else:
        return html[7:len(html)]

def is_localhost_ip(domain):
    if "127.0.0.1" in domain:
        return True
    elif "localhost" in domain:
        return True

    myaddr = socket.getaddrinfo(domain, 'http')


    if str(myaddr[0][4][0]) == "127.0.0.1":
        return True
    elif myaddr[0][4][0] == "localhost":
        return True
    
    return False

def make_ip_img(text_list,tgid):
    try:
        font = ImageFont.truetype('./font/MiSans-Regular.ttf', 40) # 设置字体及字号
        #draw = ImageDraw.Draw(image)
        text_w_list = []
        text_h_list = []
        for i in range(len(text_list)):
            text_w = font.getbbox(text_list[i])#获取长度
            text_w_list.append(text_w[2])
            text_h_list.append(text_w[3])

        img_max_w = max(text_w_list)
        img_max_h = max(text_h_list)
        img_sum_h = max(text_h_list)*len(text_list)
        #print(img_max_w,img_max_h)
        image = Image.new('RGB', (img_max_w+70,img_sum_h+140), (34,33,33)) # 设置画布大小及背景色
        draw = ImageDraw.Draw(image)
        color_fill_list = [(255, 95, 86),(255, 189, 46),(39, 201, 63)]
        color_outline_list = [(224, 68, 62),(222, 161, 35),(26, 171, 41)]
        for color_num in range(3):
            x_r = 30 + 60*color_num
            y_t=  20
            draw.ellipse(((x_r+10,y_t+10), (x_r+50,y_t+50)), fill=color_fill_list[color_num], outline=color_outline_list[color_num], width=1)

        for i in range(len(text_list)):
            draw.text((35,(i*img_max_h)+100), text_list[i], (255,255,255), font)
            #print(i*img_max_h)
        #draw.text((0,0), '22', 'black', font)
        image.save(f'./tmp/{tgid}-ip.jpg') # 保存图片
        return True
    except Exception as e:
        print(e)
        return False