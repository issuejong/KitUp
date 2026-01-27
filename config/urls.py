from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # allauth (로그인/소셜로그인)
    path("accounts/", include("allauth.urls")),

    # API
    path("api/", include("config.api_urls")),
]
