from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    actor = serializers.StringRelatedField(read_only=True)
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'timestamp', 'read']
        read_only_fields = ['id', 'actor', 'verb', 'target', 'timestamp']

    def get_target(self, obj):
        if hasattr(obj.target, 'title'):  # Post
            return f"Post: {obj.target.title}"
        elif hasattr(obj.target, 'content'):  # Comment
            return f"Comment: {obj.target.content[:50]}..."
        return str(obj.target)
