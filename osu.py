import requests
import json
import yaml
import cairosvg
import os
import sqlite3

if os.path.exists("./user/osu/data.db") is False: #初始化
    osu_con = sqlite3.connect("./user/osu/data.db")
    osu_cur = osu_con.cursor()
    sql = "CREATE TABLE IF NOT EXISTS osudb(tg_id TEXT PRIMARY KEY,osu_id TEXT)"
    osu_cur.execute(sql)
    osu_con.commit()
    # 关闭游标
    osu_cur.close()
    # 断开数据库连接
    osu_con.close()

def get_osu_img(name,mode,is_mini,tg_id): # 获取osu图片
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
        if is_mini: 
            down_url = "https://osu-sig.vercel.app/card?user={0}&mode={1}&blur=6&mini=true&w=1920&h=1117".format(str(ok_userjson['user_id']),mode) #下载地址合成
        else:
            down_url = "https://osu-sig.vercel.app/card?user={0}&mode={1}&blur=6&w=1920&h=1117".format(str(ok_userjson['user_id']),mode) #下载地址合成
        #if bottok['proxybool'] == True:
        #    proxies = bottok['proxy']
        #    down_res = requests.get(url=down_url,proxies=proxies)
        #else:
        #    down_res = requests.get(url=down_url)
        
        #with open('./tmp/osu_'+str(ok_userjson['user_id'])+'.svg',"wb") as code:
        #    code.write(down_res.content)
        cairosvg.svg2png(url=down_url, write_to='./tmp/osu_'+str(tg_id)+"_"+str(ok_userjson['user_id'])+'_'+str(mode)+'.png')
        #os.remove('./tmp/osu_'+str(ok_userjson['user_id'])+'.svg')
        return "osu_"+str(tg_id)+"_"+str(ok_userjson['user_id'])+'_'+str(mode)+".png"
    except Exception as errr:
        return False

def get_osuid(name):
    try:
        
        with open('config.yml', 'r') as f: #读取配置文件?
            bottok = yaml.load(f.read(),Loader=yaml.FullLoader)
        token = bottok['osuToken'] 
        url="https://osu.ppy.sh/api/get_user?k="+token+"&u="+str(name)
        if bottok['proxybool'] == True:
            proxies = bottok['proxy'] 
        else:
            proxies = None
        get_res = requests.get(url, proxies=proxies)
        return json.loads(get_res.text)[0]
    except Exception as err:
        return False

def sql_tg2osu_id(telegram_id):
    try:
        osu_con = sqlite3.connect("./user/osu/data.db")
        osu_cur = osu_con.cursor()
        #osu_cur.execute("INSERT INTO tg_id values(?,?)", ("", "zgq"))
        osu_cur.execute("select * from osudb where tg_id='"+str(telegram_id)+"'")
        get_out = osu_cur.fetchall()
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
        if len(get_out) == 0:
            return False
        else:
            return get_out[0][1]
    except:
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
        return False

def sql_osu2tg_id(osu_id):
    try:
        osu_con = sqlite3.connect("./user/osu/data.db")
        osu_cur = osu_con.cursor()
        #osu_cur.execute("INSERT INTO tg_id values(?,?)", ("", "zgq"))
        osu_cur.execute("select * from osudb where osu_id='"+str(osu_id)+"'")
        get_out = osu_cur.fetchall()
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
        if len(get_out) == 0:
            return False
        else:
            return get_out[0][0]
    except:
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
        return False

def sql_wq(tg_id,osu_id):
    try:
        osu_con = sqlite3.connect("./user/osu/data.db")
        osu_cur = osu_con.cursor()
        #osu_cur.execute("INSERT INTO tg_id values(?,?)", ("", "zgq"))
        osu_cur.execute("INSERT INTO osudb values(?,?)", (tg_id, osu_id))
        osu_con.commit()
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
    except:
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
        return False

def sql_del(tg_id):
    try:
        osu_con = sqlite3.connect("./user/osu/data.db")
        osu_cur = osu_con.cursor()
        #osu_cur.execute("INSERT INTO tg_id values(?,?)", ("", "zgq"))
        osu_cur.execute("DELETE FROM osudb WHERE tg_id=?", (str(tg_id),))
        osu_con.commit()
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
    except:
        # 关闭游标
        osu_cur.close()
        # 断开数据库连接
        osu_con.close()
        return False