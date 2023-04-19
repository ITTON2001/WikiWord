
from django.shortcuts import render
import requests


def main(request):
    print("main entered")
    return render(request, 'main/main.html')

#ログイントークンを取得する
def api(request):
    S = requests.Session()

    URL = "https://www.mediawiki.org/w/api.php"

    PARAMS = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    print(LOGIN_TOKEN)
    return render(request, 'main/forecast.html')