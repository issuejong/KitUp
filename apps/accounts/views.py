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
    """
    마이페이지 조회 뷰

    - 로그인한 사용자의 정보, 역할 레벨, 팀 프로젝트 참여 내역 등을 조회
    - 'account/mypage.html' 템플릿을 렌더링
    - 프로젝트 내역은 team_members -> team -> project 경로로 조회한다.
    """

    user = request.user

    # 역할별 스킬 레벨 (user_role_levels + roles)
    role_levels = user.role_levels.select_related("role").all()

    # 팀 프로젝트 참여 내역 (team_members + role + team + project)
    memberships = (
        user.team_members
            .select_related("team__project", "role")
            .order_by("-joined_at")
    )

    context = {
        "user_obj": user,
        "role_levels": role_levels,
        "memberships": memberships,
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
