from django.urls import path
from . import views

app_name = "guides"

urlpatterns = [
    # 미션/체크리스트 페이지
    path("mission/", views.mission, name="mission"),
    # 미션 카드 완료 토글
    path("card/<int:card_id>/toggle/", views.toggle_card, name="toggle_card"),
]
