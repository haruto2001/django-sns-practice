// ブラウザバックを禁止
// ※Google Chromeではフォーカスが一度でも当たっていないとブラウザバックできてしまう
window.onload = function() {
  history.pushState(null, null, null);

  window.addEventListener("popstate", function (e) {
    history.pushState(null, null, null);
    return;
  });
};