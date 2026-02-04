from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Retrospective
from .serializers import RetrospectiveReadSerializer, RetrospectiveWriteSerializer
# from .models import Reflection


@login_required
def note_list(request):
    """회고 목록"""
    # TODO: 회고 목록 로직 구현
    return render(request, "reflections/note_list.html")


@login_required
def note_create(request):
    """회고 작성"""
    # TODO: 회고 작성 로직 구현
    if request.method == "POST":
        # 폼 처리 로직
        pass
    return render(request, "reflections/note_create.html")


@login_required
def note_detail(request, note_id):
    """회고 상세"""
    # TODO: 회고 상세 로직 구현
    # note = get_object_or_404(Reflection, id=note_id)
    context = {
        "note_id": note_id,
    }
    return render(request, "reflections/note_detail.html", context)


@login_required
def note_update(request, note_id):
    """회고 수정"""
    # TODO: 회고 수정 로직 구현
    # note = get_object_or_404(Reflection, id=note_id)
    if request.method == "POST":
        # 폼 처리 로직
        pass
    context = {
        "note_id": note_id,
    }
    return render(request, "reflections/note_update.html", context)


@login_required
def note_delete(request, note_id):
    """회고 삭제"""
    # TODO: 회고 삭제 로직 구현
    # note = get_object_or_404(Reflection, id=note_id)
    if request.method == "POST":
        # note.delete()
        messages.success(request, "회고가 삭제되었습니다.")
        return redirect("reflections:note_list")
    return redirect("reflections:note_detail", note_id=note_id)

@extend_schema_view(
    list=extend_schema(summary="회고 목록 조회", tags=["Retrospectives"]),
    retrieve=extend_schema(summary="회고 상세 조회", tags=["Retrospectives"]),
    create=extend_schema(summary="회고 생성", tags=["Retrospectives"]),
    update=extend_schema(summary="회고 전체 수정", tags=["Retrospectives"]),
    partial_update=extend_schema(summary="회고 부분 수정", tags=["Retrospectives"]),
    destroy=extend_schema(summary="회고 삭제", tags=["Retrospectives"]),
)
class RetrospectiveViewSet(viewsets.ModelViewSet):
    serializer_class = RetrospectiveReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        if not u.is_authenticated:
            return Retrospective.objects.none()
        # 내 회고만
        return (
            Retrospective.objects
            .filter(user_id=self.request.user.id)
            .select_related("project", "user")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        # user는 서버에서 강제
        print("AUTH:", self.request.user, self.request.user.is_authenticated)
        serializer.save(user=self.request.user)

    def get_object(self):
        # pk 직접 접근 차단
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        obj = super().get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("본인 회고만 접근 가능합니다.")
        return obj
    
    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RetrospectiveReadSerializer
        return RetrospectiveWriteSerializer
    

    
