from django.urls import path, include

urlpatterns = [
    path("", include("apps.accounts.api_urls")),
    path("", include("apps.projects.api_urls")),
    path("", include("apps.teams.api_urls")),
    path("", include("apps.guides.api_urls")),
    path("", include("apps.reflections.api_urls")),
]
