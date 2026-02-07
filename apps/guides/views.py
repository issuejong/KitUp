from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from apps.projects.models import Project
from apps.teams.models import TeamMember
from .models import GuideCard, GuideTask, GuideTaskProgress, ProjectProgress
from .services import GuideService

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

@login_required
def mission(request):
    """사용자의 미션 페이지 (현재 프로젝트)"""
    # 사용자가 참여한 프로젝트 조회
    project = (
        Project.objects
        .filter(team__members__user=request.user, team__members__is_active=True)
        .first()
    )
    
    if not project:
        return render(request, "guides/mission.html", {"project": None})
    
    # 사용자의 역할 조회
    team_member = get_object_or_404(
        TeamMember,
        team=project.team,
        user=request.user,
        is_active=True
    )
    role = team_member.role
    
    # 해당 역할의 모든 미션 조회
    guide_cards = GuideCard.objects.filter(
        role=role,
        is_active=True
    ).prefetch_related('tasks')
    
    # 1. 모든 task 수집
    all_tasks = []
    cards_tasks_map = {}  # card_id -> tasks
    for card in guide_cards:
        card_tasks = list(card.tasks.all())
        cards_tasks_map[card.id] = card_tasks
        all_tasks.extend(card_tasks)
    
    # 2. 한 번에 모든 progress 조회 (N+1 해결)
    progress_map = {}
    for progress in GuideTaskProgress.objects.filter(
        task__in=all_tasks,
        project=project
    ):
        progress_map[progress.task_id] = progress
    
    # 각 미션의 진행도 계산
    mission_data = []
    for card in guide_cards:
        tasks = cards_tasks_map[card.id]
        completed_tasks = sum(
            1 for task in tasks 
            if progress_map.get(task.id, GuideTaskProgress()).is_completed
        )
        
        # 태스크 데이터
        task_progress_data = []
        for task in tasks:
            progress = progress_map.get(task.id)
            
            task_progress_data.append({
                'task': task,
                'is_completed': progress.is_completed if progress else False,
                'completed_at': progress.completed_at if progress else None,
            })

        is_card_completed = completed_tasks == len(tasks) and len(tasks) > 0

        mission_data.append({
            'card': card,
            'content_html': GuideService.render_markdown(card.content_md),
            'total_tasks': len(tasks),
            'completed_tasks': completed_tasks,
            'progress_percent': int((completed_tasks / len(tasks) * 100) if len(tasks) > 0 else 0),
            'task_progress_data': task_progress_data,
            'is_completed': is_card_completed,
        })
    
    # 모든 역할의 진척도 (PM/FE/BE 전부 표시)
    all_role_progress = ProjectProgress.objects.filter(
        project=project
    ).select_related('role')
    
    context = {
        'project': project,
        'role': role,
        'mission_data': mission_data,
        'all_role_progress': all_role_progress,
    }
    return render(request, "guides/mission.html", context)

@login_required
@require_POST
def toggle_card(request, card_id):
    """
    미션 카드 완료 상태 토글
    - 카드의 모든 태스크를 일괄 완료/미완료 처리
    """
    try:
        data = json.loads(request.body)
        is_completed = data.get('is_completed', False)
        
        # 현재 프로젝트 조회
        project = Project.objects.filter(
            team__members__user=request.user,
            team__members__is_active=True
        ).first()
        
        if not project:
            return JsonResponse({'success': False, 'error': 'No project'}, status=400)
        
        # 카드 조회
        card = get_object_or_404(GuideCard, id=card_id)
        
        # 카드의 모든 태스크 조회
        tasks = card.tasks.all()
        
        # 모든 태스크 완료 상태 업데이트
        for task in tasks:
            progress, created = GuideTaskProgress.objects.update_or_create(
                task=task,
                project=project,
                defaults={
                    'is_completed': is_completed,
                    'completed_at': timezone.now() if is_completed else None
                }
            )
        
        # 역할별 진척도 업데이트
        update_project_progress(project, card.role)
        
        # 업데이트된 진척도 조회
        project_progress = ProjectProgress.objects.get(project=project, role=card.role)
        
        return JsonResponse({
            'success': True,
            'progress_percent': project_progress.progress_percent,
            'role_code': card.role.code
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def update_project_progress(project, role):
    """프로젝트의 역할별 진척도 업데이트"""
    # 해당 역할의 모든 태스크 조회
    all_tasks = GuideTask.objects.filter(
        card__role=role,
        card__is_active=True
    )
    
    total_tasks = all_tasks.count()
    
    # 완료된 태스크 수
    completed_tasks = GuideTaskProgress.objects.filter(
        task__in=all_tasks,
        project=project,
        is_completed=True
    ).count()
    
    # ProjectProgress 업데이트 또는 생성
    ProjectProgress.objects.update_or_create(
        project=project,
        role=role,
        defaults={
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks
        }
    )