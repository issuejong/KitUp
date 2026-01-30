from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Custom User for StartLine.dev
    - allauth 사용 (password_hash는 Django가 내부적으로 관리)
    - 로그인 후 프로필 설정 화면에서 nickname 입력
    """

    nickname = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        help_text="서비스 내 표시 닉네임",
    )

    profile_image_url = models.TextField(
        null=True,
        blank=True,
        help_text="프로필 이미지 URL",
    )

    bio = models.TextField(
        null=True,
        blank=True,
        help_text="자기소개",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_profile_completed(self) -> bool:
        """프로필 설정 완료 여부"""
        return bool(self.nickname)

    def get_role_level(self, role_code: str) -> int:
        """특정 역할의 레벨 조회 (1~4, 없으면 0)"""
        try:
            role = Role.objects.get(code=role_code)
            user_level = self.role_levels.filter(role=role).first()
            return user_level.level if user_level else 0
        except Role.DoesNotExist:
            return 0

    def __str__(self) -> str:
        return self.nickname or self.username


class Role(models.Model):
    """
    역할 (시드 데이터, 고정)
    - PM: 기획
    - FRONTEND: 프론트엔드
    - BACKEND: 백엔드
    """

    class RoleCode(models.TextChoices):
        PM = "PM", "PM(기획)"
        FRONTEND = "FRONTEND", "프론트엔드"
        BACKEND = "BACKEND", "백엔드"

    code = models.CharField(
        max_length=20,
        unique=True,
        choices=RoleCode.choices,
        help_text="역할 코드 (PM/FRONTEND/BACKEND)",
    )

    name = models.CharField(
        max_length=30,
        help_text="역할 표시명",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"

    def __str__(self) -> str:
        return self.name


class UserRoleLevel(models.Model):
    """
    사용자별 역할 레벨 (1~4)
    - 역할별로 다른 레벨 관리
    - 설문 기반 진단, 재진단 가능
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="role_levels",
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_levels",
    )

    level = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text="실력 레벨 (1~4)",
    )

    last_diagnosed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="마지막 진단 일시",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_role_levels"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "role"],
                name="uq_user_role_level",
            ),
            models.CheckConstraint(
                check=models.Q(level__gte=1, level__lte=4),
                name="ck_user_role_level_range",
            ),
        ]
        indexes = [
            models.Index(fields=["role", "level"]),
        ]

    def __str__(self) -> str:
        return f"{self.user}:{self.role.code}=Lv.{self.level}"
