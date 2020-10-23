from rest_framework import serializers
from .models import Card, Comment
from users.models import User


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["user", "id", "url", "body", "posted_at", "card", "favorited_by"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    cards = serializers.HyperlinkedRelatedField(
        many=True, view_name="card-detail", read_only=True
    )
    comments = serializers.HyperlinkedRelatedField(
        many=True, view_name="comment-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["username", "id", "url", "cards", "comments"]


class CardSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

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
            "favorited_by",
            "comments",
        ]
