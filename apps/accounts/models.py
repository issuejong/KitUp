from django.contrib.auth.models import AbstractUser
from django.db import models


class Track(models.TextChoices):
    """트랙 선택지 (accounts, roadmaps에서 공통 사용)"""
    WEB_FRONT = "WEB_FRONT", "웹 프론트엔드"
    WEB_BACK = "WEB_BACK", "웹 백엔드"
    APP_FRONT = "APP_FRONT", "앱 프론트엔드"
    APP_BACK = "APP_BACK", "앱 백엔드"
    GAME = "GAME", "게임 개발"


class User(AbstractUser):
    """
    Custom User for StartLine.dev

    - allauth 사용
    - 로그인 후 프로필 설정 화면에서 nickname / profile_image 입력
    """

    # 프로필 정보 (로그인 직후에는 비어 있을 수 있음)
    nickname = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        help_text="서비스 내 표시 닉네임 (프로필 설정 시 입력)",
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True,
        help_text="프로필 이미지 URL 또는 media 경로",
    )

    # 공통 타임스탬프
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_profile_completed(self) -> bool:
        """
        프로필 설정 완료 여부
        - 프론트에서 /me 응답 보고 판단해도 되고
        - 백엔드에서도 재사용 가능
        """
        return bool(self.nickname)

    def get_track_level(self, track: str) -> int:
        """특정 트랙의 레벨 조회"""
        track_level = self.track_levels.filter(track=track).first()
        return track_level.level if track_level else 0

    def __str__(self) -> str:
        return self.nickname or self.username


class UserTrackLevel(models.Model):
    """유저별 트랙 레벨 (트랙별로 다른 레벨 관리)"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="track_levels",
    )
    track = models.CharField(
        max_length=20,
        choices=Track.choices,
    )
    level = models.PositiveSmallIntegerField(
        default=0,
        help_text="해당 트랙의 레벨 (0~6)",
    )
    diagnosed_at = models.DateTimeField(
        auto_now_add=True,
        help_text="레벨 진단 일시",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "track"], name="uq_user_track_level"),
        ]
        indexes = [
            models.Index(fields=["user", "track"]),
        ]

    def __str__(self) -> str:
        return f"{self.user}:{self.track}=Lv.{self.level}"
