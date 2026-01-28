from django.urls import path
from . import views

app_name = "roadmaps"

urlpatterns = [
    # 로드맵 목록
    path("", views.roadmap_list, name="roadmap_list"),
    
    # 로드맵 상세
    path("<int:pk>/", views.roadmap_detail, name="roadmap_detail"),
]
