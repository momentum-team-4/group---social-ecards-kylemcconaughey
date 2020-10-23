from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ParseError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import permissions
from .models import Card, Comment
from .serializers import CommentSerializer, CardSerializer, UserSerializer
from users.models import User
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.views import APIView, Response


"""
GET	/cards/	-	    list of cards from users you follow	
GET	/cards/me/	-	list of cards you have made	||| could use /cards/?list=mine or something like that
GET	/cards/all/	-	list of cards for everyone  |||	could use /cards/?list=all

POST /cards/	    card data	new card        |||  creates a card
GET	/cards/:id/	-	data for card with specified id	
PATCH /cards/:id/	card data	updated card    ||| updates the card with specified id
DELETE /cards/:id/	-	-	                    ||| deletes card with specified id

GET	/people/	-	list of all your "friends"	
POST /people/:id/	user by id	user info       ||| add user as a friend
DELETE /people/:id	-	-	                    ||| removes user with specified id from your friends
"""


class CardMaker(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [
        IsAuthenticated,
        CardMaker,
    ]
    parser_classes = [JSONParser, FileUploadParser]

    @action(detail=False)
    def mine(self, request):
        cards = Card.objects.filter(user=self.request.user).order_by("-posted_at")
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def all(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def image(self, request, pk, format=None):
        if "file" not in request.data:
            raise ParseError("Empty content")

        file = request.data["file"]
        post = self.get_object()

        post.image.save(file.name, file, save=True)
        return Response(status=201)

    @action(detail=True)
    def delete(self, request, format=None):
        Card.image.delete(save=True)
        return Response(status=204)

    def get_parser_classes(self):
        print(self.action)
        if self.action == "image":
            return [FileUploadParser]

        return [JSONParser]

    def get_queryset(self):
        return Card.objects.all().order_by("-posted_at")

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
