from rest_framework import serializers
from .models import Post, Comment
from users.models import User


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "id", "url", "body", "posted_at", "post", "favorited_by"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, view_name="post-detail", read_only=True
    )
    comments = serializers.HyperlinkedRelatedField(
        many=True, view_name="comment-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["username", "id", "url", "posts", "comments"]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "outer_text",
            "inner_text",
            "posted_at",
            "user",
            "id",
            "url",
            "is_public",
            "card_color",
            "border_style",
            "font_style",
            "text_align",
            "font_size",
            "favorited_by",
            "comments",
        ]
