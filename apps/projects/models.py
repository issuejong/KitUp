from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    """
    프로젝트
    - 1 project = 1 team (1:1 관계)
    - 팀 구성: PM 1명 / FE 2명 / BE 2명 (총 5명)
    """

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "임시저장"
        OPEN = "OPEN", "모집중"
        MATCHED = "MATCHED", "매칭완료"
        IN_PROGRESS = "IN_PROGRESS", "진행중"
        COMPLETED = "COMPLETED", "완료"
        ARCHIVED = "ARCHIVED", "보관됨"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_projects",
        help_text="프로젝트 생성자",
    )

    title = models.CharField(
        max_length=120,
        help_text="프로젝트 제목",
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="프로젝트 설명",
    )

    duration_weeks = models.SmallIntegerField(
        default=6,
        validators=[MinValueValidator(1)],
        help_text="프로젝트 기간 (주)",
    )

    target_team_size = models.SmallIntegerField(
        default=5,
        help_text="목표 팀 인원 (PM1/FE2/BE2 = 5명)",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        help_text="프로젝트 상태",
    )

    starts_at = models.DateField(
        null=True,
        blank=True,
        help_text="시작 예정일",
    )

    ends_at = models.DateField(
        null=True,
        blank=True,
        help_text="종료 예정일",
    )

    region = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="활동 지역 (오프라인 시)",
    )

    current_stage = models.ForeignKey(
        "guides.GuideStage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
        help_text="현재 진행 중인 가이드 단계",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "projects"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return self.title


class ProjectApplication(models.Model):
    """
    프로젝트 지원
    - 열정 레벨 (1~4) 저장
    - 지원 역할 선택
    """

    class Status(models.TextChoices):
        APPLIED = "APPLIED", "지원됨"
        CANCELLED = "CANCELLED", "취소됨"
        MATCHED = "MATCHED", "매칭됨"
        REJECTED = "REJECTED", "거절됨"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    role = models.ForeignKey(
        "accounts.Role",
        on_delete=models.PROTECT,
        related_name="applications",
        help_text="지원 역할 (PM/FRONTEND/BACKEND)",
    )

    passion_level = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        help_text="열정 레벨 (1~4, 설문 결과)",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED,
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "project_applications"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="uq_project_application",
            ),
            models.CheckConstraint(
                check=models.Q(passion_level__gte=1, passion_level__lte=4),
                name="ck_passion_level_range",
            ),
        ]
        indexes = [
            models.Index(fields=["project", "role", "status"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["passion_level"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} → {self.project} ({self.role.code})"
