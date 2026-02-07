document.addEventListener('DOMContentLoaded', function() {
    const missionCards = document.querySelectorAll('.mission_card');
    const totalMissions = missionCards.length;
    
    // 페이지 로드 시 진척도 계산
    updateProgress();
    
    missionCards.forEach(card => {
        const cardHeader = card.querySelector('.card_header');
        
        // 카드 클릭 - 펼치기/접기
        cardHeader.addEventListener('click', function(e) {
            // 체크 아이콘 클릭은 제외
            if (e.target.classList.contains('check_icon')) return;
            
            const isActive = card.classList.contains('active');
            const missionItem = card.closest('.mission_item');
            
            // 다른 모든 카드 닫기
            document.querySelectorAll('.mission_card').forEach(c => {
                c.classList.remove('active');
            });
            document.querySelectorAll('.mission_item').forEach(item => {
                item.classList.remove('active');
            });
            
            // 클릭한 카드 열기
            if (!isActive) {
                card.classList.add('active');
                missionItem.classList.add('active');
            }
        });
        
        // 체크 아이콘 클릭 시 완료 처리
        const checkIcon = card.querySelector('.check_icon');
        checkIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const card = this.closest('.mission_card');
            const missionItem = card.closest('.mission_item');
            const isCompleted = card.classList.contains('completed');
            
            if (isCompleted) {
                // 완료 취소
                card.classList.remove('completed');
                missionItem.classList.remove('completed');
                this.src = this.src.replace('check.png', 'nocheck.png');
            } else {
                // 완료 처리
                card.classList.add('completed');
                missionItem.classList.add('completed');
                this.src = this.src.replace('nocheck.png', 'check.png');
            }
            
            // 진척도 업데이트
            updateProgress();
            
            // 로컬스토리지에 저장
            saveProgress();
        });
    });
    
    // 진척도 계산 및 업데이트
    function updateProgress() {
        const completedMissions = document.querySelectorAll('.mission_card.completed').length;
        const percent = Math.round((completedMissions / totalMissions) * 100);
        
        // 현재 사용자 역할에 따라 해당 진척도 바 업데이트
        const userRole = getUserRole(); // PM, FRONTEND, BACKEND
        
        if (userRole === 'PM') {
            updateProgressBar('pm', percent);
        } else if (userRole === 'FRONTEND') {
            updateProgressBar('fe', percent);
        } else if (userRole === 'BACKEND') {
            updateProgressBar('be', percent);
        }
    }
    
    // 진척도 바 업데이트
    function updateProgressBar(role, percent) {
        const progressBar = document.getElementById(`${role}_progress`);
        const percentText = document.getElementById(`${role}_percent`);
        
        if (progressBar && percentText) {
            progressBar.style.width = `${percent}%`;
            percentText.textContent = `${percent}%`;
        }
    }
    
    // 현재 사용자 역할 가져오기
    function getUserRole() {
        // HTML에서 역할 정보를 data 속성으로 넣어야 함
        const body = document.body;
        return body.dataset.userRole || 'PM';
    }
    
    // 로컬스토리지에 진행 상황 저장
    function saveProgress() {
        const completedMissions = [];
        document.querySelectorAll('.mission_card.completed').forEach((card, index) => {
            const missionNumber = card.closest('.mission_item').dataset.number;
            completedMissions.push(missionNumber);
        });
        
        const userRole = getUserRole();
        localStorage.setItem(`mission_progress_${userRole}`, JSON.stringify(completedMissions));
    }
    
    // 로컬스토리지에서 진행 상황 불러오기
    function loadProgress() {
        const userRole = getUserRole();
        const saved = localStorage.getItem(`mission_progress_${userRole}`);
        
        if (saved) {
            const completedMissions = JSON.parse(saved);
            
            completedMissions.forEach(number => {
                const missionItem = document.querySelector(`.mission_item[data-number="${number}"]`);
                if (missionItem) {
                    const card = missionItem.querySelector('.mission_card');
                    const checkIcon = missionItem.querySelector('.check_icon');
                    
                    card.classList.add('completed');
                    missionItem.classList.add('completed');
                    if (checkIcon) {
                        checkIcon.src = checkIcon.src.replace('nocheck.png', 'check.png');
                    }
                }
            });
            
            updateProgress();
        }
    }
    
    // 페이지 로드 시 저장된 진행 상황 불러오기
    loadProgress();
});