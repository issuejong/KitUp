from django.conf import settings
from django.db import models


class Reflection(models.Model):
    class Track(models.TextChoices):
        WEB_FRONT = "WEB_FRONT", "WEB_FRONT"
        WEB_BACK = "WEB_BACK", "WEB_BACK"
        APP_FRONT = "APP_FRONT", "APP_FRONT"
        APP_BACK = "APP_BACK", "APP_BACK"
        GAME = "GAME", "GAME"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reflections")

    # nullable 허용(아이템과 느슨 연결)
    roadmap_item = models.ForeignKey(
        "roadmaps.RoadmapItem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reflections",
    )

    track = models.CharField(max_length=20, choices=Track.choices)
    content = models.TextField()
    starred = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "starred"]),
            models.Index(fields=["track", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"Reflection({self.user_id}, {self.track})"
