from django.urls import path, include

urlpatterns = [
    path("", include("apps.accounts.api_urls")),
    path("", include("apps.learning.api_urls")),
    path("", include("apps.roadmaps.api_urls")),
    path("", include("apps.reflections.api_urls")),
    path("", include("apps.teams.api_urls")),
]
