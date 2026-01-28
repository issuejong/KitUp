from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Roadmap, RoadmapItem, RoadmapTag
from .serializers import (
    RoadmapSerializer,
    RoadmapCreateSerializer,
    RoadmapItemSerializer,
    RoadmapTagSerializer,
)


# ============================================
# API ViewSets (Swagger 테스트용)
# ============================================

@extend_schema_view(
    list=extend_schema(summary="로드맵 목록 조회", tags=["Roadmaps"]),
    retrieve=extend_schema(summary="로드맵 상세 조회", tags=["Roadmaps"]),
    create=extend_schema(summary="로드맵 생성", tags=["Roadmaps"]),
    update=extend_schema(summary="로드맵 전체 수정", tags=["Roadmaps"]),
    partial_update=extend_schema(summary="로드맵 부분 수정", tags=["Roadmaps"]),
    destroy=extend_schema(summary="로드맵 삭제", tags=["Roadmaps"]),
)
class RoadmapViewSet(viewsets.ModelViewSet):
    """
    로드맵 CRUD API
    
    - GET /api/roadmaps/ : 목록 조회
    - POST /api/roadmaps/ : 생성
    - GET /api/roadmaps/{id}/ : 상세 조회
    - PUT /api/roadmaps/{id}/ : 전체 수정
    - PATCH /api/roadmaps/{id}/ : 부분 수정
    - DELETE /api/roadmaps/{id}/ : 삭제
    """
    queryset = Roadmap.objects.all().prefetch_related('items', 'tags')

    def get_serializer_class(self):
        if self.action == 'create':
            return RoadmapCreateSerializer
        return RoadmapSerializer


@extend_schema_view(
    list=extend_schema(summary="로드맵 아이템 목록 조회", tags=["Roadmap Items"]),
    retrieve=extend_schema(summary="로드맵 아이템 상세 조회", tags=["Roadmap Items"]),
    create=extend_schema(summary="로드맵 아이템 생성", tags=["Roadmap Items"]),
    update=extend_schema(summary="로드맵 아이템 전체 수정", tags=["Roadmap Items"]),
    partial_update=extend_schema(summary="로드맵 아이템 부분 수정", tags=["Roadmap Items"]),
    destroy=extend_schema(summary="로드맵 아이템 삭제", tags=["Roadmap Items"]),
)
class RoadmapItemViewSet(viewsets.ModelViewSet):
    """
    로드맵 아이템 CRUD API
    
    - GET /api/roadmap-items/ : 목록 조회
    - POST /api/roadmap-items/ : 생성
    - GET /api/roadmap-items/{id}/ : 상세 조회
    - PUT /api/roadmap-items/{id}/ : 전체 수정
    - PATCH /api/roadmap-items/{id}/ : 부분 수정
    - DELETE /api/roadmap-items/{id}/ : 삭제
    """
    queryset = RoadmapItem.objects.all().select_related('roadmap', 'resource')
    serializer_class = RoadmapItemSerializer

    @extend_schema(summary="아이템 완료 처리", tags=["Roadmap Items"])
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """아이템을 완료 상태로 변경"""
        from django.utils import timezone
        item = self.get_object()
        item.is_completed = True
        item.completed_at = timezone.now()
        item.save()
        return Response(RoadmapItemSerializer(item).data)


# ============================================
# Template Views (HTML 렌더링용 - 나중에 추가)
# ============================================

# Create your views here.
