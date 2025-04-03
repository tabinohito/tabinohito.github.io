// ヘッダーを読み込む関数
function loadHeader() {
    fetch('common_header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading header:', error);
        });
}

// フッターを読み込む関数
function loadFooter() {
    fetch('common_footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer').innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading footer:', error);
        });
}

// ページが読み込まれたら関数を呼び出す
document.addEventListener('DOMContentLoaded', () => {
    loadHeader();
    loadFooter();
});
