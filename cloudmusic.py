from typing import Any
import requests
import os


class CloudMusic:

    def __init__(self):
        self.user_token = None
        self.api_url = "https://gumusic.vercel.app{0}"
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0)"
        }
        self.request_cookies = {}

    def login(self, account: Any, key: str):
        if type(account) is int:
            request = requests.get(self.api_url.format("/login/cellphone"),
                                   f"phone={account}&password={key}").json()
        elif type(account) is str:
            request = requests.get(self.api_url.format("/login/cellphone"), f"email={account}&password={key}").json()
        else:
            raise CloudMusicLoginFailed("请输入一个正确的账号")

        # 判断登录信息是否正确且匹配，code=200 是登录成功的信号
        if int(request["code"]) == 200:
            self.user_token = request["token"]
            self.request_cookies = {
                "MUSIC_U": self.user_token
            }
        else:
            raise CloudMusicLoginFailed("账号或密码错误")

    def set_token(self, token: str):
        self.user_token = token
        self.request_cookies = {
            "MUSIC_U": self.user_token
        }

    def refresh_login(self):
        if self.user_token is None:
            raise CloudMusicNeedLogin("请先登录")
        else:
            self.request_cookies = {
                "MUSIC_U": self.user_token
            }
            request = requests.post(self.api_url.format("/login/refresh"), cookies=self.request_cookies).json()
            self.user_token = request["token"]

    # 你来写
    def save_info(self):
        pass

    # 返回一个list,具体格式:
    # [歌曲名称, 作者, 歌曲ID]
    def search(self, search_name: str) -> list:
        request = requests.get(
            self.api_url.format("/search"), f"keywords={search_name}", cookies=self.request_cookies
        ).json()
        if request["result"]["songCount"] == 0:
            raise CloudMusicSearchFailed("未找到相关歌曲")
        items = []
        for music_item in request["result"]["songs"]:
            artists = ""
            # 若有多个作者。每个作者之间会添加 ,
            for index, artists_item in enumerate(music_item["artists"]):
                if index == len(music_item["artists"]) - 1:
                    artists += artists_item["name"]
                else:
                    artists += artists_item["name"] + ","
            items.append([music_item["name"], artists, music_item["id"]])
        return items

    # 这里我直接写入到文件，若有需要可以直接拿music_data用
    def download(self, music_id: int) -> None:
        song_artists = ""
        try:
            music_detail = requests.get(
                self.api_url.format("/song/detail"), f"ids={music_id}", cookies=self.request_cookies
            ).json()["songs"][0]
        except IndexError:
            raise CloudMusicDownloadFailed("歌曲ID错误: 歌曲不存在")
        song_title = music_detail["name"]
        for index, artists_item in enumerate(music_detail["ar"]):
            if index == len(music_detail["ar"]) - 1:
                song_artists += artists_item["name"]
            else:
                song_artists += artists_item["name"] + ","

        music_download_url = requests.get(
            self.api_url.format("/song/download/url"), f"id={music_id}",
            headers=self.request_headers, cookies=self.request_cookies).json()["data"]["url"]

        if music_download_url is None:
            raise CloudMusicDownloadFailed("当前歌曲为VIP歌曲或需购买专辑，请检查登录及VIP状态后再尝试")
        music_data = requests.get(music_download_url, headers=self.request_headers,
                                  cookies=self.request_cookies).content
        if os.path.exists("./musics") is False:
            os.mkdir("./musics")
        with open(f"./musics/{song_title} - {song_artists}.mp3", "wb") as w:
            w.write(music_data)


# 异常抛出类
class CloudMusicException(Exception):
    pass


class CloudMusicLoginFailed(CloudMusicException):
    pass


class CloudMusicNeedLogin(CloudMusicException):
    pass


class CloudMusicSearchFailed(CloudMusicException):
    pass


class CloudMusicDownloadFailed(CloudMusicException):
    pass
