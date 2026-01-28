from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    # 레벨 진단 테스트
    path("test/", views.level_test, name="level_test"),
    
    # 진단 결과
    path("test/result/", views.test_result, name="test_result"),
    
    # 학습 페이지
    path("study/", views.study, name="study"),
    
    # 챗봇 (비동기)
    path("chatbot/", views.chatbot, name="chatbot"),
]
