import json
import requests

def nbnhhsh(text):
    url = 'https://lab.magiconch.com/api/nbnhhsh/guess'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }

    data = {
        "text": text
    }

    response = requests.post(url=url, headers=headers, data=data)
    json_text = response.text
    ok_json = eval(json.dumps(json.loads(json_text)))
    try:
        sc = ok_json[0]["trans"]
        gu_text = '你查询的 *'+ok_json[0]["name"]+'* 可能是:\n'
        for i in range(0, len(sc)):
            if len(sc) != i:
                gu_text += str(i+1)+'. *『'+ok_json[0]["trans"][i]+'』* \n'
            else:
                gu_text += str(i+1)+'. *『'+ok_json[0]["trans"][i]+'』* '
        return gu_text
    except:
        return "无查询结果"