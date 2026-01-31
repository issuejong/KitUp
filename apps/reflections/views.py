from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
