from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import initial_view

urlpatterns = [
    
    path("", initial_view.as_view(), name="initial"),
    path("admin/", admin.site.urls),

    # template views: HTML로 보여줄 주소들
    #   allauth (로그인/소셜로그인)
    path("accounts/", include("allauth.urls")),

    # API views: Swagger로 테스트할 주소들
    path("api/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )