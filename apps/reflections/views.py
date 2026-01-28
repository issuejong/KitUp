from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamCreateSerializer, TeamMemberSerializer


# ============================================
# API ViewSets (Swagger 테스트용)
# ============================================

@extend_schema_view(
    list=extend_schema(summary="팀 목록 조회", tags=["Teams"]),
    retrieve=extend_schema(summary="팀 상세 조회", tags=["Teams"]),
    create=extend_schema(summary="팀 생성", tags=["Teams"]),
    update=extend_schema(summary="팀 전체 수정", tags=["Teams"]),
    partial_update=extend_schema(summary="팀 부분 수정", tags=["Teams"]),
    destroy=extend_schema(summary="팀 삭제", tags=["Teams"]),
)
class TeamViewSet(viewsets.ModelViewSet):
    """
    팀 CRUD API
    
    - GET /api/teams/ : 목록 조회
    - POST /api/teams/ : 생성
    - GET /api/teams/{id}/ : 상세 조회
    - PUT /api/teams/{id}/ : 전체 수정
    - PATCH /api/teams/{id}/ : 부분 수정
    - DELETE /api/teams/{id}/ : 삭제
    """
    queryset = Team.objects.all().prefetch_related('members')

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
    """
    팀 멤버 CRUD API
    
    - GET /api/team-members/ : 목록 조회
    - POST /api/team-members/ : 생성 (팀에 멤버 추가)
    - GET /api/team-members/{id}/ : 상세 조회
    - PUT /api/team-members/{id}/ : 전체 수정
    - PATCH /api/team-members/{id}/ : 부분 수정 (역할 변경 등)
    - DELETE /api/team-members/{id}/ : 삭제 (팀에서 멤버 제거)
    """
    queryset = TeamMember.objects.all().select_related('team', 'user')
    serializer_class = TeamMemberSerializer

    @extend_schema(summary="리더로 승급", tags=["Team Members"])
    @action(detail=True, methods=['post'])
    def promote_to_leader(self, request, pk=None):
        """멤버를 리더로 승급"""
        member = self.get_object()
        member.role = TeamMember.Role.LEADER
        member.save()
        return Response(TeamMemberSerializer(member).data)


# ============================================
# Template Views (HTML 렌더링용 - 나중에 추가)
# ============================================

# Create your views here.
