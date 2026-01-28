from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OnboardingForm

@login_required
def onboarding_profile(request):
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
