from django.core.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .models import Card, Comment
from .serializers import CommentSerializer, CardSerializer, UserSerializer
from users.models import User

"""
GET	/cards/	-	    list of cards from users you follow	
GET	/cards/me/	-	list of cards you have made	||| could use /cards/?list=mine or something like that
GET	/cards/all/	-	list of cards for everyone  |||	could use /cards/?list=all

POST /cards/	    card data	new card        |||  creates a card
GET	/cards/:id/	-	data for card with specified id	
PATCH /cards/:id/	card data	updated card    ||| updates the card with specified id
DELETE /cards/:id/	-	-	                    ||| deletes card with specified id

GET	/friends/	-	list of all your "friends"	
POST /friends/	user by id	user info       ||| add user as a friend
DELETE /friends/:user_id	-	-	            ||| removes user with specified id from your friends
"""


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Card.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        raise PermissionDenied()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        serializer.save(user=self.request.user)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return User.objects.all()
