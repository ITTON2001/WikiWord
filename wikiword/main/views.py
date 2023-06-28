
from django.shortcuts import render
from django import template
import requests
import wikipediaapi


def main(request):
    print("main entered")

    #wikipediaapiのデータの言語を日本語化
    wiki_wiki = wikipediaapi.Wikipedia(
        'ja',
        #HTMLのタグ付きデータを受け取る
        extract_format=wikipediaapi.ExtractFormat.HTML
        )

    #検索ワード
    page_py = wiki_wiki.page('織田信長')

    #検索ワードを発見した時
    if page_py.exists():
        page_title = page_py.title
        page_text = page_py.text

        #リンクが貼られていた言葉のリストを作成する
        links = page_py.links
        link_word = []
        for title in sorted(links.keys()):
            link_word.append(title)

        result = []
        i = 0
        #リストの単語を調査する
        for word in link_word:
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

        
    #main.htmlに情報を返す
    return render(request, 'main/main.html', {
        'page_text': page_text, 
        'page_title': page_title,
        'res': res,
        })

"""
テスト用
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
