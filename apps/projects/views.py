from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# from .models import Project


@login_required
def dashboard(request):
    """프로젝트 대시보드 (전체)"""
    # TODO: 대시보드 로직 구현
    return render(request, "projects/dashboard.html")


@login_required
def dashboard_detail(request, project_id):
    """특정 프로젝트 대시보드"""
    # TODO: 특정 프로젝트 대시보드 로직 구현
    # project = get_object_or_404(Project, id=project_id)
    context = {
        "project_id": project_id,
    }
    return render(request, "projects/dashboard.html", context)
