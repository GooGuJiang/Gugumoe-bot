# Gugumoe-bot
![https://github.com/GooGuJiang/Gugumoe-bot]( https://i0.hdslb.com/bfs/album/18f28e3a7b5c74dbe628166ddeadc02516d3c5ce.jpg )
 
**⚠️本仓库文档未完善**

 这是咕谷酱的Telegram机器人 (咕小酱)
 是基于 [pyTelegramBotAPI](/eternnoir/pyTelegramBotAPI) 的一个 Python 机器人。
 
 ~~同时会有一堆运行Bug~~
 
 **[咕小酱在这呢!](http://t.me/gugumoe_bot)**
 
 <a href="https://count.getloli.com"><img align="center" src="https://count.getloli.com/get/@Gugumoe-bot"></a><br>

## 👉功能
| 功能 | 是否实现 |
| ------- | ------- |
|今日人品|√|
|咕|√|
|能不能好好说话?|√|
|下载SoundCloud音乐|X|
|Http.Cat|√|
|图片放大|√|
|网易云音乐下载|60%|

## 👉指令列表

|功能|指令|
| ------- | ------- |
|今日人品|/jrrp|
|咕|/gu|
|能不能好好说话|/guhhsh [需要查询的缩写]|
|下载SoundCloud音乐|/gudlsds [音乐地址]|
|获取Http.Cat图片|/httpcat [http代码]|
|图片放大[貌似没用]|/gubig [回复要放大的图片]|
|网易云音乐下载|/gunetmu [网易云音乐ID/分享链接]|

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

4. 配置 config.yml

5. 启动机器人

```bash
$ python3 main.py
```

# 😊配置文件说明
**请严格使用 YAML 的书写规范进行配置**

| 名称 | 描述 | 类型 | 举例 |
| ------- | ------- | ------- | ------- |
| botToken | Telegram 机器人 Token | str | 114514XXX:XXXX_XXXXXXX_XXXXXX |
| osuToken | OSU API KEY (暂时没用) | str | 56a3261XXXXX109XXXXX79 |
| proxybool | 是否通过代理 | bool | True |
| proxy | 代理配置 | json | {'http': 'socks5://127.0.0.1:8089','https': 'socks5://127.0.0.1:8089'} |
| apikey | deepai.org API KEY | str | 3XX6bXX9-XXXX-XXXX-XXXX-XXXXfbc7285b |
|musicapi|网易云第三方API地址| str |  http://XXXX:3000 |
|musicphone|网易云手机号|int|11451419198|
|musicpwd|网易云登录密码|str|XXXXXXXX|

**第三方API基于 [NeteaseCloudMusicApi](https://github.com/Binaryify/NeteaseCloudMusicApi) 使用网上公共API请注意安全哦！**
