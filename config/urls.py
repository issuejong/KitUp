from django.contrib import admin
from django.urls import path, include
from .views import initial_view

urlpatterns = [
    
    path("", initial_view.as_view(), name="initial"),
    path("admin/", admin.site.urls),

    # allauth (로그인/소셜로그인)
    path("accounts/", include("allauth.urls")),

    # API
    path("api/", include("config.api_urls")),
]
