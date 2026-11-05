// DOMContentLoadedイベントは、HTMLドキュメントが完全に読み込まれ、解析された後に実行されます。
document.addEventListener('DOMContentLoaded', function() {
     
     // エラーメッセージを表示するspanタグをすべて選択して、それらのリストをerrorSpans変数に代入します。
    const errorSpans = document.querySelectorAll('span');

	// errorSpansに含まれる各span要素に対して、forEachメソッドを使用して関数を実行します。
    errorSpans.forEach(function(span) {
        
        //// span要素のテキスト内容が空白でない（エラーメッセージがある）場合にチェックします。
        if (span.textContent.trim().length > 0) {
			
			// エラーメッセージがある場合、そのspan要素に'error-message'クラスを追加します。
			// これにより、CSSで定義されたエラースタイルが適用されます。
            span.classList.add('error-message');
        }
    });
});