// スタートボタン
function submitForm(event) {
    event.preventDefault(); // デフォルトのフォーム送信をキャンセル

    var form = document.getElementById("start");
    var formData = new FormData(form);

    // チェックボックスの値を取得
    var checkbox = document.querySelector('input[name="checkbox"]:checked');
    var checkboxValue = checkbox ? checkbox.value : null

    //チェックボックスの値が取得されなかったら
    if (checkboxValue === null) {
        console.error('チェックボックスが選択されていません');
        alert('ゲームモードを選択してください');
        return;
    }

    //formDataにチェックボックスの値を追加
    formData.append('checkbox', checkboxValue);

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
