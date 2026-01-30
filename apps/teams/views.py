from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamCreateSerializer, TeamMemberSerializer


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
