from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.accounts.models import Role, UserRoleLevel
from apps.projects.models import Season

from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamCreateSerializer, TeamMemberSerializer


# ================================
# Template Views (HTML 렌더링)
# ================================

@login_required
def team_apply(request):
    """
    팀 매칭 신청 페이지
    
    - 활성화된 시즌 확인
    - 팀매칭 기간인지 확인
    - 유저의 역할별 레벨 정보를 함께 전달
    - 'teams/team_apply.html' 템플릿을 렌더링
    - 딕셔너리 형태로 역할 코드와 UserRoleLevel 객체 전달
    - is_matching_period 플래그로 분기 처리
    """
    user = request.user
    season = Season.get_active_season()

    # 유저의 역할별 레벨
    role_levels = (
        UserRoleLevel.objects
        .filter(user=user)
        .select_related("role")
    )

    role_level_map = {
        rl.role.code: rl
        for rl in role_levels
    }
    
    # 팀 매칭 기간 여부
    is_matching_period = season and season.is_matching_period() if season else False

    context = {
        "user_obj": user,
        "role_levels": role_level_map,
        "season": season,
        "is_matching_period": is_matching_period,
    }

    return render(request, "teams/team_apply.html", context)


@login_required
def passion_test(request):
    """
    열정 테스트 페이지
    
    - 열정 레벨이 이미 있으면 team_status로 리다이렉트
    - 없으면 'teams/passion_test.html' 템플릿을 렌더링
    """
    if request.user.passion_level:
        # 이미 열정 테스트 완료
        return redirect("teams:team_status")
    
    return render(request, "teams/passion_test.html")

@login_required
def passion_submit(request):
    """
    열정 테스트 결과 제출 처리
    
    - POST 요청으로 열정 레벨(passion_level)을 전달받음
    - User 모델에 열정 레벨 저장
    - 제출 후 팀 매칭 결과 페이지로 리다이렉트
    """
    if request.method != "POST":
        return HttpResponseBadRequest("잘못된 요청입니다.")
    
    passion_level = request.POST.get("passion_level")
    
    request.user.passion_level = int(passion_level)
    request.user.save(update_fields=["passion_level"])
    
    return redirect("teams:team_status")


@login_required
def team_status(request):
    """
    팀 매칭 결과/대기 페이지
    
    - 팀 매칭 결과 표시
    - 시즌 정보 전달
    """
    season = Season.get_active_season()
    
    # TODO: 팀 조회 로직
    context = {
        "season": season,
    }
    return render(request, "teams/team.html", context)


# ================================
# API Views (DRF ViewSets)
# ================================


@extend_schema_view(
    list=extend_schema(summary="팀 목록 조회", tags=["Teams"]),
    retrieve=extend_schema(summary="팀 상세 조회", tags=["Teams"]),
    create=extend_schema(summary="팀 생성", tags=["Teams"]),
    update=extend_schema(summary="팀 전체 수정", tags=["Teams"]),
    partial_update=extend_schema(summary="팀 부분 수정", tags=["Teams"]),
    destroy=extend_schema(summary="팀 삭제", tags=["Teams"]),
)
class TeamViewSet(viewsets.ModelViewSet):
    """팀 CRUD API"""
    queryset = Team.objects.all().prefetch_related('members__user', 'members__role')

    def get_serializer_class(self):
        if self.action == 'create':
            return TeamCreateSerializer
        return TeamSerializer


@extend_schema_view(
    list=extend_schema(summary="팀 멤버 목록 조회", tags=["Team Members"]),
    retrieve=extend_schema(summary="팀 멤버 상세 조회", tags=["Team Members"]),
    create=extend_schema(summary="팀 멤버 추가", tags=["Team Members"]),
    update=extend_schema(summary="팀 멤버 전체 수정", tags=["Team Members"]),
    partial_update=extend_schema(summary="팀 멤버 부분 수정", tags=["Team Members"]),
    destroy=extend_schema(summary="팀 멤버 삭제", tags=["Team Members"]),
)
class TeamMemberViewSet(viewsets.ModelViewSet):
    """팀 멤버 CRUD API"""
    queryset = TeamMember.objects.all().select_related('team', 'user', 'role')
    serializer_class = TeamMemberSerializer
