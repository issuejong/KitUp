from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

from apps.projects.models import Season
from apps.projects.services import TeamMatchingService


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


# ================================
# 팀 매칭 관리 API
# ================================

@permission_required('projects.add_project', raise_exception=True)
@require_POST
def run_team_matching(request, season_id):
    """
    팀 매칭 알고리즘 실행 (관리자만)
    
    POST /projects/matching/{season_id}/run/
    
    Returns:
        JSON: 매칭 결과 통계
    """
    try:
        season = Season.objects.get(id=season_id)
    except Season.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'시즌 ID {season_id}를 찾을 수 없습니다.',
        }, status=404)
    
    # 팀매칭 기간 확인
    if not season.is_matching_period():
        return JsonResponse({
            'success': False,
            'error': '현재 팀매칭 기간이 아닙니다.',
        }, status=400)
    
    try:
        result = TeamMatchingService.run_matching(season_id)
        
        return JsonResponse({
            'success': True,
            'message': f'✅ 팀 매칭 완료! {result["teams_created"]}개 팀 생성',
            'data': {
                'teams_created': result['teams_created'],
                'total_users_matched': result['total_users_matched'],
                'pm_matched': result['pm_matched'],
                'fe_matched': result['fe_matched'],
                'be_matched': result['be_matched'],
                'total_unmatched': result['total_unmatched'],
                'unmatched_details': result['unmatched'],
            }
        })
    
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': f'❌ 매칭 실패: {str(e.message)}',
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'❌ 예상치 못한 오류: {str(e)}',
        }, status=500)
