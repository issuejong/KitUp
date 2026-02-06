// mission.js

document.addEventListener('DOMContentLoaded', function() {
    const missionCards = document.querySelectorAll('.mission_card');
    
    missionCards.forEach(card => {
        card.addEventListener('click', function() {
            const isActive = this.classList.contains('active');
            
            // 다른 모든 카드 닫기
            missionCards.forEach(c => {
                c.classList.remove('active');
            });
            
            // 클릭한 카드 토글
            if (!isActive) {
                this.classList.add('active');
            }
        });
        
        // 체크 아이콘 클릭 시 완료 처리
        const checkIcon = card.querySelector('.check_icon');
        checkIcon.addEventListener('click', function(e) {
            e.stopPropagation(); // 카드 클릭 이벤트 방지
            
            const card = this.closest('.mission_card');
            const isCompleted = card.classList.contains('completed');
            
            if (isCompleted) {
                card.classList.remove('completed');
                this.src = this.src.replace('check.png', 'nocheck.png');
            } else {
                card.classList.add('completed');
                this.src = this.src.replace('nocheck.png', 'check.png');
            }
        });
    });
});