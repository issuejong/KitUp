from django.contrib.auth.models import AbstractUser
from django.db import models


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

    profile_image = models.TextField(
        null=True,
        blank=True,
        help_text="프로필 이미지 URL 또는 media 경로",
    )

    # 학습 레벨
    user_level = models.PositiveSmallIntegerField(
        default=0,
        help_text="사용자 학습 레벨 (0~6)",
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

    def __str__(self) -> str:
        return self.nickname or self.username
