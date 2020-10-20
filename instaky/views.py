from django.core.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Post, Comment
from .serializers import CommentSerializer, PostSerializer, UserSerializer
from users.models import User

"""
GET	/cards/	-	list of cards from users you follow	
GET	/cards/me/	-	list of cards you have made	||| could use /cards/?list=mine or something like that
GET	/cards/all/	-	list of cards for everyone |||	could use /cards/?list=all
POST	/cards/	card data	new card |||  creates a card
GET	/cards/:id/	-	data for card with specified id	
PATCH	/cards/:id/	card data	updated card ||| updates the card with specified id
DELETE	/cards/:id/	-	-	||| deletes card with specified id
GET	/friends/	-	list of all your "friends"	
POST	/friends/	user by id	user info ||| add user as a friend
DELETE	/friends/:user_id	-	-	||| removes user with specified id from your friends
"""


class WroteOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user == request.user:
            return True

        return False


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [
        WroteOrRead,
    ]

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        raise PermissionDenied()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        WroteOrRead,
    ]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        serializer.save(author=self.request.user)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [
        WroteOrRead,
    ]

    def get_queryset(self):
        return User.objects.all()
