from rest_framework import serializers
from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 'author_id']


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for likes"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts with nested comments and likes"""
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.ReadOnlyField(source='author.id')
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 'created_at', 
                  'updated_at', 'comments', 'likes', 'comments_count', 'likes_count', 'is_liked']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 'author_id']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts"""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
