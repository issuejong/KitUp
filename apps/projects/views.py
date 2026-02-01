from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# from .models import Project


@login_required
def dashboard(request):
    """현재 프로젝트 대시보드"""
    # TODO: 대시보드 로직 구현
    return render(request, "projects/dashboard.html")


@login_required
def dashboard_detail(request, project_id):
    """나의 현재 프로젝트 대시보드"""
    # TODO: 단 하나뿐 나의 프로젝트 대시보드
    # project = get_object_or_404(Project, id=project_id)
    context = {
        "project_id": project_id,
    }
    return render(request, "projects/dashboard.html", context)


@login_required
def dashboard_update(request, project_id):
    """나의 현재 프로젝트 대시보드 수정"""
    # TODO: 프로젝트 정보 수정 로직
    # project = get_object_or_404(Project, id=project_id, created_by=request.user)
    if request.method == "POST":
        # 정보 업데이트
        messages.success(request, "프로젝트가 업데이트되었습니다.")
        return render(request, "projects/dashboard.html")
    
    context = {
        "project_id": project_id,
    }
    return render(request, "projects/dashboard_update.html", context)


@login_required
def project_list(request):
    """지난 프로젝트 리스트"""
    # TODO: 지난 프로젝트 리스트 로직 구현
    # projects = request.user.created_teams.all()
    context = {}
    return render(request, "projects/project_list.html", context)


@login_required
def project_detail(request, project_id):
    """지난 프로젝트 상세"""
    # TODO: 지난 프로젝트 상세 로직 구현
    # project = get_object_or_404(Project, id=project_id)
    context = {
        "project_id": project_id,
    }
    return render(request, "projects/project_detail.html", context)


@login_required
def kitup_list(request):
    """모든 KITUP 프로젝트 리스트"""
    # TODO: 모든 프로젝트 리스트 로직 구현
    context = {}
    return render(request, "projects/kitup_list.html", context)


@login_required
def kitup_detail(request, project_id):
    """모든 KITUP 프로젝트 상세"""
    # TODO: 모든 프로젝트 상세 로직 구현
    # project = get_object_or_404(Project, id=project_id)
    context = {
        "project_id": project_id,
    }
    return render(request, "projects/kitup_detail.html", context)
