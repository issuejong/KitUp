from django.contrib import admin

from .models import Project, ProjectApplication


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "status", "duration_weeks", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "project", "user", "role", "passion_level", "status", "applied_at"]
    list_filter = ["status", "role", "passion_level"]
    search_fields = ["project__title", "user__nickname"]
    ordering = ["-applied_at"]
