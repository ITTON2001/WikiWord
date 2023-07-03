// スタートボタン
function submitForm(event) {
    event.preventDefault(); // デフォルトのフォーム送信をキャンセル

    var form = document.getElementById("start");
    var formData = new FormData(form);

    // チェックボックスの値を取得
    var checkboxes = document.querySelectorAll('input[name="checkbox"]:checked');
    var checkboxValues = Array.from(checkboxes).map(function(checkbox) {
        return checkbox.value;
    });

    //チェックボックスの値が取得されなかったら
    if (checkboxValues.length === 0) {
        console.error('チェックボックスが選択されていません');
        alert('ゲームモードを選択してください');
        return;
    }

    //formDataにチェックボックスの値を追加
    formData.append('checkbox', checkboxValues);

    // フォームデータを送信
    fetch(form.action, {
        method: form.method,
        body: formData,
    }).then(function(response) {
        // ページ遷移
        window.location.href = "/maingame/";
        console.log("ページ遷移・・・完了")
    }).catch(function(error) {
        console.error('エラー:', error);
    });
}

// モード選択
function toggleCheckboxes(clickedCheckbox) {
    var checkboxes = document.getElementsByName("checkbox");
    checkboxes.forEach(function(checkbox) {
        if (checkbox !== clickedCheckbox) {
            checkbox.checked = false;
        }
    });
}