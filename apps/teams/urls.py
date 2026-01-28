from django.urls import path
from . import views

app_name = "teams"

urlpatterns = [
    # 팀 목록 (매칭 페이지)
    path("", views.team_list, name="team_list"),
    
    # 팀 생성
    path("create/", views.team_create, name="team_create"),
    
    # 팀 상세
    path("<int:pk>/", views.team_detail, name="team_detail"),
    
    # 팀 가입
    path("<int:pk>/join/", views.team_join, name="team_join"),
    
    # 팀 탈퇴
    path("<int:pk>/leave/", views.team_leave, name="team_leave"),
]
