from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Role, UserRoleLevel, TechStack


class UserRoleLevelInline(admin.TabularInline):
    model = UserRoleLevel
    extra = 0
    fields = ["role", "level", "last_diagnosed_at"]
    readonly_fields = ["last_diagnosed_at"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id", "username", "nickname", "email", "is_staff", "created_at"]
    list_filter = ["is_staff", "is_active", "created_at"]
    search_fields = ["username", "nickname", "email"]
    ordering = ["-created_at"]
    inlines = [UserRoleLevelInline]
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ("프로필 정보", {"fields": ("nickname", "profile_image", "bio", "tech_stacks")}),
    )


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "created_at"]
    list_filter = ["category"]
    search_fields = ["name"]
    ordering = ["category", "name"]
    fieldsets = [
        ("기본 정보", {"fields": ["name", "category"]}),
    ]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "created_at"]
    search_fields = ["code", "name"]
    ordering = ["code"]


@admin.register(UserRoleLevel)
class UserRoleLevelAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "role", "level", "last_diagnosed_at", "updated_at"]
    list_filter = ["role", "level"]
    search_fields = ["user__nickname", "user__username"]
    ordering = ["-updated_at"]
