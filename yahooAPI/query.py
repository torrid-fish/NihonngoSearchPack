import json
from urllib import request
from SearchPack.yahooAPI.key import APPID

# The translation from kanji to furigana with yahoo api
URL = "https://jlp.yahooapis.jp/FuriganaService/V2/furigana"

def askFurigana(query):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Yahoo AppID: {}".format(APPID),
    }
    param_dic = {
      "id": "1234-1",
      "jsonrpc": "2.0",
      "method": "jlp.furiganaservice.furigana",
      "params": {
        "q": query,
        "grade": 1
      }
    }
    params = json.dumps(param_dic).encode()
    req = request.Request(URL, params, headers)
    with request.urlopen(req) as res:
        body = res.read()
    return json.loads(body.decode())