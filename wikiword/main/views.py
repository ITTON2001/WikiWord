
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

page_py = None  # 初期値を設定

def tittle(request):
    return render(request, 'main/title.html')


#初期の文字を設定
def select_first_word():
    import requests
    #wikipediaからランダムに記事を受け取るAPI
    S = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": "1",
        "rnnamespace": "0",
    }

    #要求したデータを受け取る
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    #データをランダムに受け取る
    RANDOMS = DATA["query"]["random"]
    selected_word = RANDOMS[0]["title"]
           
    print("初期："+selected_word)
    return selected_word

#ゴールの文字を設定
def select_goal_word():
    import requests
    #wikipediaからランダムに記事を受け取るAPI
    S = requests.Session()
    URL = "https://ja.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnlimit": "1",
        "rnnamespace": "0",
    }

    #要求したデータを受け取る
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    #データをランダムに受け取る
    RANDOMS = DATA["query"]["random"]
    goal_word = RANDOMS[0]["title"]
           
    print("目標："+goal_word)
    return goal_word
        
#wikipediaapiの処理
def wikipediaapi(selected_word_receive):
    import wikipediaapi
    # wikipediaapiのデータの言語を日本語化
    wiki_wiki = wikipediaapi.Wikipedia(
        'ja',
        # HTMLのタグ付きデータを受け取る
        extract_format=wikipediaapi.ExtractFormat.HTML
    )

    # 検索ワード
    page_py = wiki_wiki.page(selected_word_receive)    

    # デフォルト値を設定
    page_title = ''
    page_text = ''
    res = ''

    #検索ワードを発見した時
    if page_py.exists():
        page_title = page_py.title
        page_text = page_py.text

        #リンクが貼られていた言葉のリストを作成する
        links = page_py.links
        link_word = []
        for title in sorted(links.keys()):
            link_word.append(title)

        #print(link_word)
        sorted_link_word = sorted(link_word, key=len, reverse=True)
        #print(sorted_link_word)

        #文章生成プログラム
        result = []
        i = 0
        #リストの単語を調査する
        for word in sorted_link_word:
            #リストの単語がpage_textにあるか調べ、その出現位置を代入する
            start_index = page_text.find(word)
            #あったとき
            if start_index != -1:
                #出現位置と文字の長さを足すことで対象の単語の終了位置を代入する
                end_index = start_index + len(word)
                #出現位置の所までの文章をbefに入れる
                bef = page_text[:start_index]
                #終了位置から後ろの文章をaftに入れる
                aft = page_text[end_index:]
                #対象の言葉をspanタグに変更しbefとaftをつなげた文章をresultリストに追加する
                result.append(bef + '<span style="cursor: pointer;" onclick="handleClick()">' + word + '</span>' + aft)
                # 次の単語の検索に使用するため、更新された文章を調査対象の文章に設定する
                page_text = result[i]  
                #回数の更新
                i += 1

        #言葉の調査が終わったとき
        if result:
            res = result[-1]  # 最後の要素を取得

    #検索ワードが見つからなかった場合
    else:
        page_text = 'ページが見つかりませんでした。'

    return page_title,page_text,res

@csrf_exempt
def main(request):
    print("main entered")
         
    if request.method == "POST":
        clicked_word = request.POST.get("word", "")
        print(clicked_word)  # コンソールに表示して確認する（デバッグ用）
        #wikipediaapiで受け取ったデータを変数にそれぞれ入れる
        page_title,page_text,res = wikipediaapi(clicked_word)
        #print(page_title)
        #print(res)
        #javascriptへデータを送る
        return JsonResponse({
        'page_text': page_text, 
        'page_title': page_title,
        'res': res,
        })
    else:
        #初期の文字を受け取る
        selected_word = select_first_word()
        #目標の文字を受け取る
        goal_word = select_goal_word()
        #wikipediaapiで受け取ったデータを変数にそれぞれ入れる
        page_title,page_text,res = wikipediaapi(selected_word)

    #main.htmlに情報を返す
    return render(request, 'main/main.html', {
        'page_text': page_text, 
        'page_title': page_title,
        'res': res,
        'goal_word':goal_word,
        })


"""
文章生成プログラムのテスト用
def main(request):
    text = "私はみかんが好きです。しかしメロンも食べます。"
    words = ["みかん", "メロン"]

    result = []
    i = 0
    for word in words:
        
        start_index = text.find(word)
        if start_index != -1:
            end_index = start_index + len(word)
            bef = text[:start_index]
            aft = text[end_index:]
            result.append(bef + '<span style="cursor: pointer;" onclick="handleClick()">' + word + '</span>' + aft)
            text = result[i]  # 次の単語の検索に使用するため、更新された部分文字列を代入
            i += 1

    if result:
        res = result[-1]  # 最後の要素を取得

    return render(request, 'main/main.html', {'res': res})
"""
