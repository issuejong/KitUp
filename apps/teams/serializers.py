from rest_framework import serializers
from .models import Team, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """팀 멤버 Serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'team', 'user', 'username', 'role', 'role_display', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    """팀 기본 Serializer"""
    members = TeamMemberSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'created_by', 'created_by_username',
            'created_at', 'members', 'member_count'
        ]
        read_only_fields = ['id', 'created_at']

    def get_member_count(self, obj) -> int:
        return obj.members.count()


class TeamCreateSerializer(serializers.ModelSerializer):
    """팀 생성용 Serializer (간소화)"""

    class Meta:
        model = Team
        fields = ['id', 'name', 'created_by']
        read_only_fields = ['id']
