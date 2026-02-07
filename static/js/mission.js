document.addEventListener('DOMContentLoaded', function() {
    const missionCards = document.querySelectorAll('.mission_card');
    const userRole = document.body.dataset.userRole || 'PM'; // PM, FRONTEND, BACKEND
    
    // 페이지 로드 시 저장된 진척도 불러오기
    loadProgress();
    
    missionCards.forEach(card => {
        const cardHeader = card.querySelector('.card_header');
        
        // 카드 클릭 - 펼치기/접기
        cardHeader.addEventListener('click', function(e) {
            if (e.target.classList.contains('check_icon')) return;
            
            const isActive = card.classList.contains('active');
            const missionItem = card.closest('.mission_item');
            
            document.querySelectorAll('.mission_card').forEach(c => {
                c.classList.remove('active');
            });
            document.querySelectorAll('.mission_item').forEach(item => {
                item.classList.remove('active');
            });
            
            if (!isActive) {
                card.classList.add('active');
                missionItem.classList.add('active');
            }
        });
        
        // 체크 아이콘 클릭
        const checkIcon = card.querySelector('.check_icon');
        checkIcon.addEventListener('click', function(e) {
            e.stopPropagation();
            
            const card = this.closest('.mission_card');
            const missionItem = card.closest('.mission_item');
            const missionNumber = missionItem.dataset.number;
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
            
            // 로컬스토리지에 저장 & 진척도 업데이트
            saveProgress();
            updateProgress();
        });
    });
    
    // 진척도 계산 및 업데이트
    function updateProgress() {
        const totalMissions = missionCards.length;
        const completedMissions = document.querySelectorAll('.mission_card.completed').length;
        const percent = Math.round((completedMissions / totalMissions) * 100);
        
        updateProgressBar(userRole, percent);
    }
    
    // 진척도 바 업데이트
    function updateProgressBar(role, percent) {
        let barId, percentId;
        
        if (role === 'PM') {
            barId = 'pm_progress';
            percentId = 'pm_percent';
        } else if (role === 'FRONTEND') {
            barId = 'fe_progress';
            percentId = 'fe_percent';
        } else if (role === 'BACKEND') {
            barId = 'be_progress';
            percentId = 'be_percent';
        }
        
        const progressBar = document.getElementById(barId);
        const percentText = document.getElementById(percentId);
        
        if (progressBar && percentText) {
            progressBar.style.width = `${percent}%`;
            percentText.textContent = `${percent}%`;
        }
    }
    
    // 로컬스토리지에 진행 상황 저장
    function saveProgress() {
        const completedMissions = [];
        document.querySelectorAll('.mission_item').forEach(item => {
            const card = item.querySelector('.mission_card');
            if (card.classList.contains('completed')) {
                const missionNumber = item.dataset.number;
                completedMissions.push(missionNumber);
            }
        });
        
        localStorage.setItem(`mission_progress_${userRole}`, JSON.stringify(completedMissions));
    }
    
    // 로컬스토리지에서 진행 상황 불러오기
    function loadProgress() {
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
        }
        
        // 진척도 업데이트
        updateProgress();
    }
});