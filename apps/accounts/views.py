from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from .forms import OnboardingForm, ProfileUpdateForm


@login_required
def onboarding_profile(request):
    """온보딩: 최초 프로필 설정"""
    if request.method == "POST":
        form = OnboardingForm(
            request.POST,
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
def profile_update(request):
    """프로필 수정"""
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect("accounts:mypage")
    else:
        form = ProfileUpdateForm(instance=request.user)

    context = {"form": form}
    return render(request, "account/profile_update.html", context)


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
