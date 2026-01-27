from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("onboarding/profile/", views.onboarding_profile, name="onboarding_profile"),
]
