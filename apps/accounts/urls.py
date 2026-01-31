from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # 온보딩
    path("onboarding/profile/", views.onboarding_profile, name="onboarding_profile"),
    
    # 레벨 진단 (Test)
    path("level-test/", views.level_test, name="level_test"),  # level_test.html
    path("level-test/result/", views.test_result, name="test_result"),  # test_result.html
    
    # 마이페이지
    path("mypage/", views.mypage, name="mypage"),  # mypage.html
    
    # 프로필 수정
    path("profile/edit/", views.profile_edit, name="profile_edit"),  # profile_edit.html
    
    # 회원 탈퇴
    path("withdraw/", views.withdraw, name="withdraw"),
]
