from django.contrib import admin

from .models import Season, Project, ProjectApplication


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "is_active", "matching_start", "matching_end", "project_start", "project_end"]
    list_filter = ["status", "is_active", "created_at"]
    search_fields = ["name"]
    ordering = ["-created_at"]
    actions = ["activate_season", "deactivate_season"]
    
    def activate_season(self, request, queryset):
        """시즌 활성화 (이전 활성 시즌은 자동 비활성화)"""
        # 모든 시즌 비활성화
        Season.objects.all().update(is_active=False)
        # 선택된 시즌만 활성화
        queryset.update(is_active=True)
        self.message_user(request, "시즌이 활성화되었습니다.")
    
    def deactivate_season(self, request, queryset):
        """시즌 비활성화"""
        queryset.update(is_active=False)
        self.message_user(request, "시즌이 비활성화되었습니다.")
    
    activate_season.short_description = "✅ 선택된 시즌 활성화"
    deactivate_season.short_description = "❌ 선택된 시즌 비활성화"


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
