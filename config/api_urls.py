from django.urls import path, include

urlpatterns = [
    path("", include("accounts.api_urls")),
    path("", include("learning.api_urls")),
    path("", include("roadmaps.api_urls")),
    path("", include("reflections.api_urls")),
    path("", include("teams.api_urls")),
]
