from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    # 프로젝트 대시보드
    path("dashboard/", views.dashboard, name="dashboard"),  # dashboard.html
    path("dashboard/<int:project_id>/", views.dashboard_detail, name="dashboard_detail"),  # dashboard.html (특정 프로젝트)
]
