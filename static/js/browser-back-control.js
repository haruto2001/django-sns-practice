// 新規投稿ページ，投稿編集ページ，コメント作成ページ以外のページでブラウザバックを禁止
// ※Google Chromeではフォーカスが一度でも当たっていないとブラウザバックできてしまう
if !( document.URL.match(create) || document.URL.match(update) ){
  window.onload = function() {
    history.pushState(null, null, null);

    window.addEventListener("popstate", function (e) {
      history.pushState(null, null, null);
      return;
    });
  };
}