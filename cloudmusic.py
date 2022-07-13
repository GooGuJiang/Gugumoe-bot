import requests
import os


# 异常抛出类
class CloudMusicException(Exception):
    pass


class CloudMusic:

    def __init__(self):
        self.token = None
        self.api_url = "https://gumusic.vercel.app{0}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0)"
        }
        self.cookies = {}

    def login(self, account, key: str) -> bool:
        # 这里的try是为了分出手机号和邮箱登录
        try:
            phone_number = int(account)
            request = requests.get(self.api_url.format("/login/cellphone"),
                                   f"phone={phone_number}&password={key}").json()
        except ValueError:
            request = requests.get(self.api_url.format("/login/cellphone"), f"email={account}&password={key}").json()

        # 判断登录信息是否正确且匹配，code200 即是登录成功的信号
        if int(request["code"]) == 200:
            self.token = request["token"]
            self.cookies = {
                "MUSIC_U": self.token
            }
            return True
        else:
            raise CloudMusicException("账号或密码错误")

    def set_token(self, token: str) -> None:
        self.token = token
        self.cookies = {
            "MUSIC_U": self.token
        }

    def refresh_login(self) -> bool:
        if self.token is None:
            raise CloudMusicException("请先登录")
        else:
            self.cookies = {
                "MUSIC_U": self.token
            }
            request = requests.post(self.api_url.format("/login/refresh"), cookies=self.cookies).json()
            self.token = request["token"]
            return True

    # 你来写
    def save_info(self):
        pass

    # 返回一个list,具体格式:
    # [歌曲名称, 作者, 歌曲ID]
    def search(self, search_name: str) -> list:
        request = requests.get(self.api_url.format("/search"), f"keywords={search_name}", cookies=self.cookies).json()
        items = []
        for music_item in request["result"]["songs"]:
            artists = ""
            for index, artists_item in enumerate(music_item["artists"]):
                if index == len(music_item["artists"]) - 1:
                    artists += artists_item["name"]
                else:
                    artists += artists_item["name"] + "/"
            items.append([music_item["name"], artists, music_item["id"]])
        return items

    # 这里我直接写入到文件，若有需要可以直接拿music_data用
    def download(self, music_id: int) -> None:
        song_detail = {}
        try:
            music_detail = requests.get(self.api_url.format("/song/detail"), f"ids={music_id}", cookies=self.cookies).json()["songs"][0]
        except IndexError:
            raise CloudMusicException("歌曲ID错误: 歌曲不存在")
        song_detail["name"] = music_detail["name"]
        song_detail["artists"] = ""
        for index, artists_item in enumerate(music_detail["ar"]):
            if index == len(music_detail["ar"]) - 1:
                song_detail["artists"] += artists_item["name"]
            else:
                song_detail["artists"] += artists_item["name"] + ","
        music_download_url = requests.get(self.api_url.format("/song/download/url"), f"id={music_id}",
                                          headers=self.headers, cookies=self.cookies).json()["data"]["url"]
        if music_download_url is None:
            raise CloudMusicException("当前歌曲为VIP歌曲或需购买专辑，请检查登录及VIP状态后再尝试")
        music_data = requests.get(music_download_url, headers=self.headers, cookies=self.cookies).content
        if os.path.exists("./musics") is False:
            os.mkdir("./musics")
        if os.path.exists(f"./musics/{song_detail['name']} - {song_detail['artists']}.mp3") is False:
            with open(f"./musics/{song_detail['name']} - {song_detail['artists']}.mp3", "wb") as w:
                w.write(music_data)
