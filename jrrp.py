import datetime
import random
import sqlite3
import time
import os
import requests

def jrrp_oneload():
    # 检查 `./user/jrrp` 路径是否存在，不存在则创建
    path = "./user/jrrp"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    jrrp_sql_con = sqlite3.connect(path + "/data.db")
    jrrp_sql_cur = jrrp_sql_con.cursor()
    sql = "CREATE TABLE jrrp(tg_id TEXT PRIMARY KEY,nub INTEGER,time TEXT)"
    jrrp_sql_cur.execute(sql)
    # 关闭游标
    jrrp_sql_cur.close()
    # 断开数据库连接
    jrrp_sql_con.close()

if not os.path.exists("./user/jrrp/data.db"): #初始化
    jrrp_oneload()

def get_random(userid):
    try:
        # 使用 `大气噪声` 算法进行随机数生成
        url = 'https://www.random.org/integers/?num=1&min=0&max=100&col=1&base=10&format=plain&rnd=new'
        res = requests.get(url)
        return res.text.strip("\n")
    except:
        out_hash = hash(str(datetime.datetime.now())+str(userid))
        if out_hash < 0:
            out_hash=out_hash*-1
        out_str = int(str(out_hash)[0:2])

        if out_str >= 98:        
            if random.randint(0,1) == 1:
                return 100
            else:
                return out_str
        elif out_str <= 11:
            if random.randint(0,1) == 1:
                return random.randint(0,10)
            else:
                return out_str
        else:
            return out_str

def jrrp_text_init(nub_in):
    nub = int(nub_in)
    return {
        nub >= 0:   "抽大奖¿",
        nub >= 20:  f"{nub} 这数字太....要命了",
        nub >= 40:  f"还好还好只有 {nub}",
        nub >= 50:  "五五开！",
        nub >= 60:  "今天是 非常¿ 不错的一天呢!",
        nub >= 70:  "哇,人品还挺好的!",
        nub >= 90:  "今天的人品非常不错呢",
        nub == 100: "100 人品好评!!!"
    }[True]

def jrrp_text(nub_in):
    nub = int(nub_in)
    return {
        nub >= 0:   "*抽大奖¿*",
        nub >= 20:  f"{nub} 这数字太....要命了",
        nub >= 40:  f"还好还好只有 {nub}",
        nub >= 50:  "五五开！",
        nub >= 60:  "今天是 *非常¿* 不错的一天呢!",
        nub >= 70:  "哇,人品还挺好的!",
        nub >= 90:  "今天的人品非常不错呢",
        nub == 100: "*100 人品好评!!!*"
    }[True]

def jrrp_get(tgid):
    jrrp_sql_con = sqlite3.connect("./user/jrrp/data.db")
    jrrp_sql_cur = jrrp_sql_con.cursor()
    gu_out_data = None
    get_sql = jrrp_sql_con.execute("select * from jrrp where tg_id = {0}".format(tgid))
    for data in get_sql:
        gu_out_data = data
    
    if gu_out_data is None:
        random_get = get_random(tgid)
        jrrp_sql_cur.execute("INSERT INTO jrrp values(?,?,?)", (int(tgid), random_get, time.strftime("%y-%m-%d", time.localtime())))
        jrrp_sql_con.commit()
        # 关闭游标
        jrrp_sql_cur.close()
        # 断开数据库连接
        jrrp_sql_con.close()
        return random_get

    if gu_out_data[2] == time.strftime("%y-%m-%d", time.localtime()):
        jrrp_sql_cur.close()
        # 断开数据库连接
        jrrp_sql_con.close()
        return gu_out_data[1]
    else:
        random_get = get_random(tgid)
        jrrp_sql_cur.execute("UPDATE jrrp SET nub=? WHERE tg_id=?", (random_get, tgid))
        jrrp_sql_con.commit()
        jrrp_sql_cur.execute("UPDATE jrrp SET time=? WHERE tg_id=?", (time.strftime("%y-%m-%d", time.localtime()), tgid))
        jrrp_sql_con.commit()
        # 关闭游标
        jrrp_sql_cur.close()
        # 断开数据库连接
        jrrp_sql_con.close()
        return random_get
    #print(get_sql)
