from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class LearningResource(models.Model):
    class Platform(models.TextChoices):
        YOUTUBE = "YOUTUBE", "YOUTUBE"
        INFLEARN = "INFLEARN", "INFLEARN"
        VELOG = "VELOG", "VELOG"
        BLOG = "BLOG", "BLOG"
        ETC = "ETC", "ETC"

    class ContentType(models.TextChoices):
        VIDEO = "VIDEO", "VIDEO"
        ARTICLE = "ARTICLE", "ARTICLE"
        COURSE = "COURSE", "COURSE"

    class Track(models.TextChoices):
        WEB_FRONT = "WEB_FRONT", "WEB_FRONT"
        WEB_BACK = "WEB_BACK", "WEB_BACK"
        APP_FRONT = "APP_FRONT", "APP_FRONT"
        APP_BACK = "APP_BACK", "APP_BACK"
        GAME = "GAME", "GAME"

    title = models.CharField(max_length=200)
    url = models.TextField(null=True, blank=True)

    platform = models.CharField(max_length=50, choices=Platform.choices, null=True, blank=True)
    content_type = models.CharField(max_length=20, choices=ContentType.choices)
    track = models.CharField(max_length=20, choices=Track.choices)

    level_min = models.PositiveSmallIntegerField(default=0)
    level_max = models.PositiveSmallIntegerField(default=6)

    estimated_time = models.PositiveIntegerField(null=True, blank=True)
    learning_style = models.CharField(max_length=50, null=True, blank=True)

    tags = models.ManyToManyField(Tag, through="LearningResourceTag", related_name="resources")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["platform"]),
            models.Index(fields=["content_type"]),
            models.Index(fields=["track"]),
            models.Index(fields=["level_min", "level_max"]),
        ]

    def __str__(self) -> str:
        return self.title


class LearningResourceTag(models.Model):
    resource = models.ForeignKey(LearningResource, on_delete=models.CASCADE, related_name="resource_tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="resource_tags")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["resource", "tag"], name="uq_learning_resource_tags"),
        ]
        indexes = [
            models.Index(fields=["tag"]),
        ]
