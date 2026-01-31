from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .forms import OnboardingForm, ProfileUpdateForm
from .models import User


@require_GET
def check_username(request):
    """아이디 중복 확인 API"""
    username = request.GET.get("username", "").strip()
    
    if not username:
        return JsonResponse({"available": False, "message": "아이디를 입력해주세요."})
    
    if len(username) < 4:
        return JsonResponse({"available": False, "message": "아이디는 4자 이상이어야 합니다."})
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({"available": False, "message": "이미 사용 중인 아이디입니다."})
    
    return JsonResponse({"available": True, "message": "사용 가능한 아이디입니다."})


@require_GET
def check_email(request):
    """이메일 중복 확인 API"""
    email = request.GET.get("email", "").strip()
    
    if not email:
        return JsonResponse({"available": False, "message": "이메일을 입력해주세요."})
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({"available": False, "message": "이미 사용 중인 이메일입니다."})
    
    return JsonResponse({"available": True, "message": "사용 가능한 이메일입니다."})


@login_required
def level_test(request):
    """레벨 진단 테스트"""
    # TODO: 레벨 테스트 로직 구현
    return render(request, "accounts/level_test.html")


@login_required
def test_result(request):
    """레벨 테스트 결과"""
    # TODO: 테스트 결과 로직 구현
    return render(request, "accounts/test_result.html")


@login_required
def profile_edit(request):
    """프로필 수정"""
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect("accounts:mypage")
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {"form": form}
    return render(request, "accounts/profile_edit.html", context)


@login_required
def onboarding_profile(request):
    """온보딩: 최초 프로필 설정"""
    if request.method == "POST":
        form = OnboardingForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = OnboardingForm(instance=request.user)

    context = {"form": form}
    return render(request, "account/onboarding_profile.html", context)


@login_required
def mypage(request):
    """마이페이지"""
    user = request.user
    role_levels = user.role_levels.select_related("role").all()
    
    context = {
        "user": user,
        "role_levels": role_levels,
    }
    return render(request, "account/mypage.html", context)


@login_required
def withdraw(request):
    """회원 탈퇴"""
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "회원 탈퇴가 완료되었습니다.")
        return redirect("/")

    return render(request, "account/withdraw.html")
