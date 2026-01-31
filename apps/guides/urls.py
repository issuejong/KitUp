from django.urls import path
from . import views

app_name = "guides"

urlpatterns = [
    # 미션/체크리스트 페이지
    path("mission/", views.mission, name="mission"),  # mission.html
    path("mission/<int:project_id>/", views.mission_detail, name="mission_detail"),  # mission.html (특정 프로젝트)
]
