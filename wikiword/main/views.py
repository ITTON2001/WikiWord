
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django import template
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openpyxl,random

# 初期値を設定
page_py = None  
mode = None

#タイトル画面
@csrf_exempt
def title(request):
    #モード選択用
    if 'checkbox' in request.POST:
        #チェックボックスのデータを受け取る
        checkboxes = request.POST.getlist('checkbox')
        print("モード選択")
        print(checkboxes[0])

        #モードに応じて目標の文字を受け取る
        if checkboxes[0] == "1":           
            #国モード
            goal_word = easy_goal_word()
        elif checkboxes[1] == "2":
            #wikiモード
            goal_word = select_goal_word()
        else:
            print("エラーです")

        # セッションにgoal_wordを保存
        request.session['goal_word'] = goal_word

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

#簡単な単語を設定
def easy_goal_word():

    #更新するExcelシート番号（左から0,1,2)
    Sheet_Num = 0

    """ Excelファイル読込(以下編集不要) """
    #Excelファイル
    EExcelFileName = "main/data/country.xlsx"
    #ワークブック読込
    workbook = openpyxl.load_workbook(EExcelFileName)
    #ワークシート読込
    select_worksheet = workbook.sheetnames[Sheet_Num]
    worksheet = workbook[select_worksheet]
    
    # セルの範囲からデータを取得
    cell_range = worksheet["B2:B260"]
    data = [cell.value for row in cell_range for cell in row]
    country_data = random.choice(data)
    print("目標："+country_data)

    return country_data

#wikipediaapiの処理
def wikipediaapi(selected_word_receive):
    import wikipediaapi
    # wikipediaapiのデータの言語を日本語化
    wiki_wiki = wikipediaapi.Wikipedia(
    language='ja',
    extract_format=wikipediaapi.ExtractFormat.HTML,
    user_agent='CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'
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

        #リンクのワードを長い順に並べる
        sorted_link_word = sorted(link_word, key=len, reverse=True)
        #print(sorted_link_word)

        #文章生成プログラム
        result = []
        saved_words = []
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

                #リンクのワードを一時別の変数に保存
                saved_words.append(word) 
                #順番を与えたtaskを置く
                word = "[task"+str(i)+"]"

                #wordをspanタグで囲みbefとaftをつなげた文章をresultリストに追加する
                result.append(bef + '<span style="cursor: pointer;" onclick="handleClick()">' + word + '</span>' + aft)
                # 次の単語の検索に使用するため、更新された文章を調査対象の文章に設定する
                page_text = result[i]  
                #回数の更新
                i += 1

        #言葉の調査が終わったとき
        if result:
            res = result[-1]  # 最後の要素を取得
            
            #taskの修正作業
            #taskの順番に応じて保存したリンクのワードに置き換えていく
            for i, word in enumerate(saved_words):
                res = res.replace(f"[task{i}]", word)

            #脚注・注釈・出典は取得できないため削除
            res = res.replace("脚注", "").replace("注釈", "").replace("出典", "")
            #print(res)

    #検索ワードが見つからなかった場合
    else:
        page_text = 'ページが見つかりませんでした。'

    return page_title,page_text,res


#メインの画面
@csrf_exempt
def main(request):
    print("main entered")    
         
    #単語クリック用
    if 'word' in request.POST:
        clicked_word = request.POST.get("word", "")
        print(clicked_word)  # コンソールに表示して確認する（デバッグ用）
        #wikipediaapiで受け取ったデータを変数にそれぞれ入れる
        page_title,page_text,res = wikipediaapi(clicked_word)
        #print(page_title)
        #print(res)
        #javascriptへデータを返す
        return JsonResponse({
        'page_text': page_text, 
        'page_title': page_title,
        'res': res,
        })
    else:
        # セッションからgoal_wordを取得
        goal_word = request.session.get('goal_word')
        print("受け取った目標データ："+goal_word)

        #初期の文字を受け取る
        selected_word = select_first_word()
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
    text = "私はみかん会社が好きです。しかしメロンも食べます。でもみかんも食べます"
    words = ["みかん会社","みかん", "メロン"]

    result = []
    saved_words = []
    i = 0
    for word in words:
        start_index = text.find(word)
        if start_index != -1:
            end_index = start_index + len(word)
            bef = text[:start_index]
            aft = text[end_index:]

            
            saved_words.append(word) 
            word = "[task"+str(i)+"]"

            result.append(bef + '<span style="cursor: pointer;" onclick="handleClick()">' + word + '</span>' + aft)
            text = result[i]  # 次の単語の検索に使用するため、更新された部分文字列を代入
            i += 1

    if result:
        res = result[-1]  # 最後の要素を取得

        j = 0
        for i, word in enumerate(saved_words):
            res = res.replace(f"[task{i}]", word)
            j += 1
        print(res)

    return render(request, 'main/main.html', {'res': res})
"""
