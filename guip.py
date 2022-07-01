from icmplib import traceroute
from icmplib import ping
from qqwry import QQwry
import socket
import re
czip = QQwry()
czip.load_file('./ip_data/qqwry.dat')


def gu_traceroute(ip): # ip路由
    try:
        gu_tmp = ""
        hops = traceroute(str(ip),count=1,fast=True,timeout=0.8)
        last_distance = 0
        for hop in hops:
            if last_distance + 1 != hop.distance:
                gu_tmp += f'{hop.distance}  {hop.address}   {czip.lookup(hop.address)[0]}({czip.lookup(hop.address)[1]})  {hop.avg_rtt} ms\n'
                last_distance = hop.distance
        return gu_tmp.strip('\n')
    except:
        return False

def gu_ping(ip):# ping 测试
    try:
        gu_tmp = ""
        hops = ping(str(ip), count=4, interval=0.2)
        for nub in range(len(hops.rtts)):
            gu_tmp += f"{nub+1}  {hops.address}  {round(hops.rtts[nub],2)} ms\n"
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
