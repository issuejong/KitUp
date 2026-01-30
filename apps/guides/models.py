from django.conf import settings
from django.db import models


class GuideStage(models.Model):
    """
    가이드 단계
    - 팀플 진행 순서를 단계별로 정의
    - code는 시드/운영용 안정적 식별자
    """

    code = models.CharField(
        max_length=40,
        unique=True,
        help_text="단계 코드 (예: S01_KICKOFF, S02_ERD)",
    )

    title = models.CharField(
        max_length=120,
        help_text="단계 제목",
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="단계 설명",
    )

    order_no = models.IntegerField(
        default=0,
        help_text="정렬 순서",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="활성화 여부",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "guide_stages"
        ordering = ["order_no"]
        indexes = [
            models.Index(fields=["order_no"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"[{self.order_no}] {self.title}"


class GuideCard(models.Model):
    """
    가이드 카드
    - 각 단계(stage)에서 역할별로 제공되는 상세 가이드
    - 마크다운 형식 콘텐츠
    """

    stage = models.ForeignKey(
        GuideStage,
        on_delete=models.CASCADE,
        related_name="cards",
    )

    role = models.ForeignKey(
        "accounts.Role",
        on_delete=models.CASCADE,
        related_name="guide_cards",
        help_text="대상 역할 (PM/FRONTEND/BACKEND)",
    )

    title = models.CharField(
        max_length=120,
        help_text="카드 제목",
    )

    content_md = models.TextField(
        help_text="상세 가이드 내용 (마크다운)",
    )

    order_no = models.IntegerField(
        default=0,
        help_text="정렬 순서",
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guide_cards"
        ordering = ["stage", "role", "order_no"]
        indexes = [
            models.Index(fields=["stage", "role", "order_no"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.stage.code} - {self.role.code}: {self.title}"


class GuideTask(models.Model):
    """
    가이드 태스크 (체크리스트 항목)
    - 각 카드에 포함된 세부 할 일
    - 퀘스트 형식으로 진행
    """

    card = models.ForeignKey(
        GuideCard,
        on_delete=models.CASCADE,
        related_name="tasks",
    )

    title = models.CharField(
        max_length=140,
        help_text="태스크 제목",
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="태스크 상세 설명",
    )

    order_no = models.IntegerField(
        default=0,
        help_text="정렬 순서",
    )

    is_required = models.BooleanField(
        default=True,
        help_text="필수 여부",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "guide_tasks"
        ordering = ["card", "order_no"]
        indexes = [
            models.Index(fields=["card", "order_no"]),
        ]

    def __str__(self) -> str:
        return f"{self.card.title} - {self.title}"


class GuideTaskProgress(models.Model):
    """
    가이드 태스크 진행 상황
    - 프로젝트 × 사용자 × 태스크 별 완료 여부
    """

    task = models.ForeignKey(
        GuideTask,
        on_delete=models.CASCADE,
        related_name="progress",
    )

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="task_progress",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="task_progress",
    )

    is_completed = models.BooleanField(
        default=False,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guide_task_progress"
        constraints = [
            models.UniqueConstraint(
                fields=["task", "project", "user"],
                name="uq_task_project_user",
            ),
        ]
        indexes = [
            models.Index(fields=["project", "user"]),
        ]

    def __str__(self) -> str:
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.task.title} ({self.user})"
