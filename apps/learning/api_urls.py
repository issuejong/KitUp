from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadmapViewSet, RoadmapItemViewSet

router = DefaultRouter()
router.register(r'roadmaps', RoadmapViewSet, basename='roadmap')
router.register(r'roadmap-items', RoadmapItemViewSet, basename='roadmap-item')

urlpatterns = [
    path('', include(router.urls)),
]
