// 直前に閲覧していたページのURLの末尾を取得
var ref = document.referrer;
var stringArray = ref.split('/');
// 編集画面から詳細画面に遷移した場合のみブラウザバックを禁止
if ( stringArray[stringArray.length-1] == 'update' ) {
  history.pushState(null, null, location.href);
  window.addEventListener('popstate', (e) => {
    history.go(1);
  })
};