from django.contrib import admin

from .models import GuideStage, GuideCard, GuideTask, GuideTaskProgress


class GuideCardInline(admin.TabularInline):
    model = GuideCard
    extra = 0
    fields = ["role", "title", "order_no", "is_active"]


class GuideTaskInline(admin.TabularInline):
    model = GuideTask
    extra = 0
    fields = ["title", "order_no", "is_required"]


@admin.register(GuideStage)
class GuideStageAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "title", "order_no", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["code", "title"]
    ordering = ["order_no"]
    inlines = [GuideCardInline]


@admin.register(GuideCard)
class GuideCardAdmin(admin.ModelAdmin):
    list_display = ["id", "stage", "role", "title", "order_no", "is_active"]
    list_filter = ["stage", "role", "is_active"]
    search_fields = ["title"]
    ordering = ["stage__order_no", "role", "order_no"]
    inlines = [GuideTaskInline]


@admin.register(GuideTask)
class GuideTaskAdmin(admin.ModelAdmin):
    list_display = ["id", "card", "title", "order_no", "is_required"]
    list_filter = ["is_required", "card__stage"]
    search_fields = ["title"]
    ordering = ["card__stage__order_no", "card__order_no", "order_no"]


@admin.register(GuideTaskProgress)
class GuideTaskProgressAdmin(admin.ModelAdmin):
    list_display = ["id", "task", "project", "user", "is_completed", "completed_at"]
    list_filter = ["is_completed", "project"]
    search_fields = ["task__title", "user__nickname"]
    ordering = ["-updated_at"]
