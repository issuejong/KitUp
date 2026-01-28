from rest_framework import serializers
from .models import Roadmap, RoadmapItem, RoadmapTag


class RoadmapTagSerializer(serializers.ModelSerializer):
    """로드맵 태그 Serializer"""
    tag_name = serializers.CharField(source='tag.name', read_only=True)

    class Meta:
        model = RoadmapTag
        fields = ['id', 'roadmap', 'tag', 'tag_name']
        read_only_fields = ['id']


class RoadmapItemSerializer(serializers.ModelSerializer):
    """로드맵 아이템 Serializer"""
    resource_title = serializers.CharField(source='resource.title', read_only=True)

    class Meta:
        model = RoadmapItem
        fields = [
            'id', 'roadmap', 'resource', 'resource_title',
            'order_no', 'is_completed', 'completed_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RoadmapSerializer(serializers.ModelSerializer):
    """로드맵 기본 Serializer"""
    items = RoadmapItemSerializer(many=True, read_only=True)
    track_display = serializers.CharField(source='get_track_display', read_only=True)

    class Meta:
        model = Roadmap
        fields = [
            'id', 'user', 'track', 'track_display', 'level',
            'current_index', 'is_completed', 'created_at', 'items'
        ]
        read_only_fields = ['id', 'created_at']


class RoadmapCreateSerializer(serializers.ModelSerializer):
    """로드맵 생성용 Serializer (간소화)"""

    class Meta:
        model = Roadmap
        fields = ['id', 'user', 'track', 'level']
        read_only_fields = ['id']
