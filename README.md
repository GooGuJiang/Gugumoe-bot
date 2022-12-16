<div align="center">

![https://github.com/GooGuJiang/Gugumoe-bot]( https://i0.hdslb.com/bfs/album/18f28e3a7b5c74dbe628166ddeadc02516d3c5ce.jpg )


# Gugumoe-bot

 这是咕谷酱的Telegram机器人 (咕小酱)
 是基于 [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) 的一个 Python 机器人。
 
 ~~同时会有一堆运行Bug~~
 
 **咕小酱在这呢👉[@gugumoe_bot](http://t.me/gugumoe_bot)**
 
 <a href="https://count.getloli.com"><img align="center" src="https://count.getloli.com/get/@Gugumoe-bot"></a><br>

![Alt](https://repobeats.axiom.co/api/embed/1931234205856e05e4269eba31551c98b6eb632c.svg "Repobeats analytics image")

</div>

<div align="center">



## **⚠️本仓库文档未完善**

</div>


# 👉功能
+ 今日人品 ✅
+ 咕 ✅
+ 能不能好好说话? ✅
+ OSU查询功能 ✅
+ Http.Cat ✅
+ IP 测试 ✅
+ 网易云音乐下载 ❌

# 💁‍♀️ 怎么部署?
1. 确保 `python` 的版本为 3.x

2. 将本仓库 `clone` 到本地:

```bash
$ git clone https://github.com/GooGuJiang/Gu-Random-Image.git
```

3. 安装所需库

```bash
$ pip install -r requirements.txt
```

4. 执行初始化

```bash
$ python3 main.py
```

5. 配置 config.yml

6. 启动机器人

```bash
$ python3 main.py
```

## ⚠️注意事项
在使用该机器人之前，请先安装 ***`GTK+ Runtime Environment`***！否则会出现部分功能 **无法使用、运行报错** 等问题！

[GTK+ For Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)

[Linux解决方案](https://gmoe.cc/419.html)

# 👉指令列表

|指令|功能|
| ------- | ------- |
|gu | 咕咕咕! |
|gu_eat | 生成一张吃头像贴纸|
|gu_5000choyen | 生成一张 想要5000兆日元 贴纸|
|jrrp | 今日人品？|
|guhhsh | 能不能好好说话?|
|httpcat | Http.Cat|
|moetrace  | 番剧截图搜索|
|guosu_help | OSU功能帮助菜单|
|guip_ping | Ping|
|guip_traceroute | 路由跟踪|

# 😊配置文件说明
**请严格使用 YAML 的书写规范进行配置**

| 名称 | 描述 | 类型 | 举例 |
| ------- | ------- | ------- | ------- |
| botToken | Telegram 机器人 Token | str | 114514XXX:XXXX_XXXXXXX_XXXXXX |
| osuToken | OSU API KEY  | str | 56a3261XXXXX109XXXXX79 |
| proxybool | 是否通过代理 | bool | True |
| proxy | 代理配置 | json | {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'} |
|musicapi|网易云第三方API地址(暂时没用)| str |  http://XXXX:3000 |
|musicphone|网易云手机号(暂时没用)|int|11451419198|
|musicpwd|网易云登录密码(暂时没用)|str|XXXXXXXX| 

<div align="center">

> ### **第三方API基于 [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 使用网上公共API请注意安全哦！**

</div>
