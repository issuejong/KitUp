from django.urls import path
from . import views

urlpatterns = [
    path("onboarding/profile/", views.onboarding_profile, name="onboarding_profile"),
]
