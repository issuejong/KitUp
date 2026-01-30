from django.conf import settings
from django.db import models


class Retrospective(models.Model):
    """
    회고
    - 프로젝트별 개인 회고 작성
    - 마크다운 형식
    """

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="retrospectives",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="retrospectives",
    )

    title = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text="회고 제목",
    )

    content_md = models.TextField(
        help_text="회고 내용 (마크다운)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "retrospectives"
        indexes = [
            models.Index(fields=["project", "user"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.project}: {self.title or '회고'}"
