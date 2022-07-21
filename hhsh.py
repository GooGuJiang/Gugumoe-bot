import requests

def nbnhhsh(text):
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    }
    response = requests.post(url=url,headers=headers,data={"text": text})
    ok_json = response.json()
    try:
        sc = ok_json[0]["trans"]
        gu_text = f'你查询的 *{ok_json[0]["name"]}* 可能是:\n'
        for i in range(0, len(sc)):
            t = ok_json[0]["trans"][i]
            gu_text += f"{i+1}. *『{t}』* " + ("\n" if len(sc) != i else "")
        return gu_text
    except Exception:
        return "无查询结果"