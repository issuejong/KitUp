from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# from .models import Guide


@login_required
def mission(request):
    """미션/체크리스트 페이지"""
    # TODO: 미션 로직 구현
    return render(request, "guides/mission.html")


@login_required
def mission_detail(request, project_id):
    """특정 프로젝트 미션 페이지"""
    # TODO: 특정 프로젝트 미션 로직 구현
    context = {
        "project_id": project_id,
    }
    return render(request, "guides/mission.html", context)
