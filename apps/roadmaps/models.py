from django.conf import settings
from django.db import models

from apps.accounts.models import Track


class Roadmap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roadmaps")
    track = models.CharField(max_length=20, choices=Track.choices)

    level = models.PositiveSmallIntegerField()
    current_index = models.PositiveIntegerField(default=0)

    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # include-only 태그(선호/방향)
    tags = models.ManyToManyField("learning.Tag", through="RoadmapTag", related_name="roadmaps")

    class Meta:
        indexes = [
            models.Index(fields=["user", "track", "is_completed"]),
        ]

    def __str__(self) -> str:
        return f"Roadmap({self.user_id}, {self.track})"


class RoadmapTag(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name="roadmap_tags")
    tag = models.ForeignKey("learning.Tag", on_delete=models.CASCADE, related_name="roadmap_tags")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["roadmap", "tag"], name="uq_roadmap_tags"),
        ]
        indexes = [
            models.Index(fields=["tag"]),
        ]


class RoadmapItem(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name="items")
    resource = models.ForeignKey(
        "learning.LearningResource",
        on_delete=models.PROTECT,
        related_name="roadmap_items",
        help_text="리소스 삭제 시 과거 로드맵 기록 보호 위해 PROTECT 권장",
    )

    order_no = models.PositiveIntegerField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["roadmap", "order_no"], name="uq_roadmap_items_order_no"),
        ]
        indexes = [
            models.Index(fields=["roadmap", "is_completed"]),
        ]

    def __str__(self) -> str:
        return f"RoadmapItem({self.roadmap_id}, #{self.order_no})"
