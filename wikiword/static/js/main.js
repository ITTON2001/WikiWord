//セキュリティのためクッキーを受け取る
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// クリックイベントの処理
function handleClick() {
    // クリックされた言葉を取得する
    var clickedWord =  event.target.textContent;
    console.log("クリックしたワード：" + clickedWord);

    //FormDataオブジェクトを作成し、appendメソッドを使用して単語を追加
    var form = new FormData();
    form.append('word', clickedWord);

    //fetch関数を使用して、POSTリクエストを送信
    fetch('/maingame/', {
        method: 'POST',
        body: form,
        //リクエストヘッダーにCSRFトークンを含めるために、'X-CSRFToken'ヘッダーを設定します。これにより、リクエストはCSRF保護を通過できる
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        //レスポンスをJSON形式で解析
        .then(response => response.json())
        .then(data => {
            let goalWord = document.getElementById('goal-word').getAttribute('data-goal-word');
            // 受け取ったデータを使用してHTMLを再構築する
            let html = '';
            html += `
                    <h1>${data.page_title}</h1>
                    <p>${data.res}</p>
                `;
            //目標に辿り着いたとき
            if (goalWord === data.page_title) {
                html += "<p>正しい</p>";
            }
            document.getElementById('main-text').innerHTML = html;
        })
        //エラーが発生した場合はコンソールにエラーメッセージを表示
        .catch(error => {
            console.error('Error:', error);
        });
}
