from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Retrospective
from .serializers import RetrospectiveReadSerializer, RetrospectiveWriteSerializer
from .forms import RetrospectiveForm

from apps.projects.models import Project
from apps.teams.models import TeamMember

@login_required
def note_list(request):
    """
    회고 목록 조회
    쿼리스트링: 
      q: 검색
      roles: 스택 필터링 ("BACKEND", "PM" 식의 복수 선택 가능, none은 개인 회고 조회)
      bookmarked: 북마크 필터링
      sort: 정렬 키워드 (new, old, title)
    """
    # TODO: 회고 목록 로직 구현
    qs = (
        Retrospective.objects
        .filter(user = request.user)  # 해당 유저의 회고만
        .select_related("project")    # 
        .order_by("-created_at")      # 시간 최신순
    )

    # 검색(제목/본문/프로젝트명)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) | 
            Q(content_md__icontains=q) | 
            Q(project__name__icontains=q)
        )
    
    # 스택 필터
    role_codes  = request.GET.getlist("roles")
    if role_codes :
        get_personnal_retro = "none" in role_codes 

        role_project_ids = (
            TeamMember.objects
            .filter(user=request.user, role__code__in=role_codes )
            .values_list("team__project_id", flat=True)
            .distinct()
        )

        if get_personnal_retro and role_project_ids:
            qs = qs.filter(
                Q(project__isnull=True) | 
                Q(project_id__in = role_project_ids)
            )
        elif get_personnal_retro:
            qs = qs.filter(project__isnull=True)
        elif role_project_ids:
            qs = qs.filter(project_id__in = role_project_ids)

    # 북마크 필터
    bookmarked = request.GET.get("bookmarked")
    if bookmarked in ("1", "true", "True"):
        qs = qs.filter(bookmarked=True)

    # 정렬
    sort = request.GET.get("sort", "new")
    if sort == "old":
        qs = qs.order_by("created_at")
    elif sort == "title":
        qs = qs.order_by("title")
    else:
        qs = qs.order_by("-created_at")
    
    my_projects = (
        Project.objects
        .filter(member__user=request.user)
        .distinct()
        .order_by("name")
    )

    context = {
        "notes" : qs,
        "my_projects": my_projects, # 내 프로젝트 조회 -> 필터에 보여주기
        "q" : q,
        "bookmarked": bookmarked,
        "sort": sort,
    }
    return render(request, "reflections/note_list.html", context)


@login_required
def note_create(request):
    """회고 작성"""
    # TODO: 회고 작성 로직 구현
    if request.method == "POST":
        form = RetrospectiveForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "회고가 작성되었습니다.")
            return redirect("reflections:note_detail", note_id=note.id)
    else:
        form = RetrospectiveForm()

    context = {"form": form}
    return render(request, "reflections/note_create.html", context)


@login_required
def note_detail(request, note_id):
    """회고 상세"""
    # TODO: 회고 상세 로직 구현
    note = get_object_or_404(Retrospective, id=note_id, user=request.user)
    context = {
        "note": note,
    }
    return render(request, "reflections/note_detail.html", context)


@login_required
def note_update(request, note_id):
    """회고 수정"""
    # TODO: 회고 수정 로직 구현
    note = get_object_or_404(Retrospective, id=note_id, user=request.user)

    if request.method == "POST":
        form = RetrospectiveForm(request.POST, instance=note)
        if form.is_valid():
            form.save
            messages.success(request, "회고가 수정되었습니다.")
            return redirect("reflections:note_detail", note_id = note.id)
    else:
        form = RetrospectiveForm(instance=note)
        
    context = {
        "note": note,
        "form": form,
    }
    return render(request, "reflections/note_update.html", context)


@login_required
def note_delete(request, note_id):
    """회고 삭제"""
    # TODO: 회고 삭제 로직 구현
    note = get_object_or_404(Retrospective, id=note_id)
    if request.method == "POST":
        note.delete()
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
    

    
