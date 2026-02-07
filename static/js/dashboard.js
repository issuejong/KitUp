document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('reportModal');
    const openBtn = document.querySelector('.btn_report'); 
    const closeBtns = document.querySelectorAll('.close-btn');

    // 팝업 열기
    if(openBtn) {
        openBtn.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex'; 
        });
    }

    // 팝업 닫기
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    });

    // 배경 클릭 시 닫기
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});