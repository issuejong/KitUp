from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.accounts.models import UserRoleLevel

from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamCreateSerializer, TeamMemberSerializer


# ================================
# Template Views (HTML 렌더링)
# ================================

@login_required
def team_apply(request):
    """
    팀 매칭 신청 페이지
    
    - 유저의 역할별 레벨 정보를 함께 전달
    - 'teams/team_apply.html' 템플릿을 렌더링
    - 딕셔너리 형태로 역할 코드와 UserRoleLevel 객체 전달
    """
    user = request.user

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

    context = {
        "user_obj": user,
        "role_levels": role_level_map,
    }

    return render(request, "teams/team_apply.html", context)


@login_required
def passion_test(request):
    """열정 테스트 페이지"""
    # TODO: 열정 테스트 로직 구현
    return render(request, "teams/passion_test.html")


@login_required
def team_status(request):
    """팀 매칭 결과/대기 페이지"""
    # TODO: 팀 매칭 상태 로직 구현
    return render(request, "teams/team.html")


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
