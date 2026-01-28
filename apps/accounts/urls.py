from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # 온보딩
    path("onboarding/profile/", views.onboarding_profile, name="onboarding_profile"),
    
    # 마이페이지
    path("mypage/", views.mypage, name="mypage"),
    
    # 프로필 수정
    path("profile/", views.profile_update, name="profile_update"),
    
    # 회원 탈퇴
    path("withdraw/", views.withdraw, name="withdraw"),
]
