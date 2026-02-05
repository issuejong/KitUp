# reflections/serializers.py
from rest_framework import serializers
from .models import Retrospective


class RetrospectiveReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.nickname", read_only=True)
    project_id = serializers.IntegerField(source="project.id", read_only=True)

    class Meta:
        model = Retrospective
        fields = [
            "id",
            "project_id",
            "user",
            "username",
            "title",
            "content_md",
            "bookmarked",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", 
            "project_id",
            "user", 
            "username", 
            "created_at", 
            "updated_at"
        ]
    def validate_content_md(self, value):
        if not value.strip():
            raise serializers.ValidationError("내용은 비어 있을 수 없습니다.")
        return value


class RetrospectiveWriteSerializer(serializers.ModelSerializer):
    # 입력은 project FK를 그대로 받는게 Swagger에서 제일 단순합니다. (정수)
    class Meta:
        model = Retrospective
        fields = ["project", "title", "content_md", "bookmarked"]
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
        }