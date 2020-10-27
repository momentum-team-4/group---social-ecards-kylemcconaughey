from rest_framework import serializers
from users.models import User
from .models import Card, Comment


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    liked_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "id", "url", "body", "posted_at", "card", "liked_by"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    cards = serializers.HyperlinkedRelatedField(
        many=True, view_name="card-detail", read_only=True
    )
    comments = serializers.HyperlinkedRelatedField(
        many=True, view_name="comment-detail", read_only=True
    )
    followers = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "id", "url", "cards", "comments", "followers"]


class UserDisplaySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id", "url"]


class CardSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Card
        fields = [
            "user",
            "is_public",
            "outer_text",
            "inner_text",
            "image",
            "posted_at",
            "id",
            "url",
            "card_color",
            "border_style",
            "font_family",
            "font_style",
            "text_align",
            "font_size",
            "liked_by",
            "comments",
        ]
