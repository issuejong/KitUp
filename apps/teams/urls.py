from django.urls import path
from . import views

app_name = "teams"

urlpatterns = [
    # 팀 매칭 신청
    path("apply/", views.team_apply, name="team_apply"),  # team_apply.html
    
    # 열정 테스트 (팀플 신청 시)
    path("passion-test/", views.passion_test, name="passion_test"),  # passion_test.html
    
    # 팀 매칭 결과/대기 화면
    path("status/", views.team_status, name="team_status"),  # team.html
]
