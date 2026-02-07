from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.projects.models import Project
from apps.teams.models import TeamMember
from .models import GuideCard, GuideTaskProgress, ProjectProgress


@login_required
def mission(request):
    """미션 페이지"""
    project = Project.objects.filter(
        team__members__user=request.user,
        team__members__is_active=True
    ).first()
    
    if not project:
        return render(request, "guides/mission.html", {"project": None})
    
    team_member = get_object_or_404(
        TeamMember,
        team=project.team,
        user=request.user,
        is_active=True
    )
    role = team_member.role
    
    # 역할별 미션 카드
    guide_cards = GuideCard.objects.filter(
        role=role,
        is_active=True
    ).order_by('order_no').prefetch_related('tasks')
    
    # 미션 데이터 구성
    mission_data = []
    for card in guide_cards:
        tasks = card.tasks.all()
        
        # 완료된 태스크 개수
        completed_count = GuideTaskProgress.objects.filter(
            task__in=tasks,
            project=project,
            is_completed=True
        ).count()
        
        # 카드 완료 여부
        is_card_completed = completed_count == tasks.count() if tasks.count() > 0 else False
        
        task_progress_data = []
        for task in tasks:
            progress = GuideTaskProgress.objects.filter(
                task=task,
                project=project
            ).first()
            
            task_progress_data.append({
                'task': task,
                'is_completed': progress.is_completed if progress else False,
            })
        
        mission_data.append({
            'card': card,
            'task_progress_data': task_progress_data,
            'is_completed': is_card_completed,
        })
    
    # 모든 역할의 진척도
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