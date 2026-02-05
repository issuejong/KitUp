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
        # TODO 테스트용 nullable
        # 플젝 외의 개인 회고의 목적 있으면 nullable 유지
        null=True, blank=True,
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

    bookmarked = models.BooleanField(
        default= False,
        # TODO 회고인데 찜 -> 어감 이상함, 즐겨찾기나 북마크로 수정
        help_text="찜 여부"
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
