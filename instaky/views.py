from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User

from .models import Card, Comment
from .serializers import (
    CardSerializer,
    CommentSerializer,
    UserDisplaySerializer,
    UserSerializer,
)

"""
GET	/cards/	-	    list of all cards
GET	/cards/mine/	-	list of cards you have made	||| could use /cards/?list=mine or something like that
GET	/cards/all/	-	list of cards for everyone  |||	could use /cards/?list=all
GET /cards/following/ list of cards from people you follow

POST /cards/	    card data	new card        |||  creates a card
GET	/cards/:id/	-	data for card with specified id	
PATCH /cards/:id/	card data	updated card    ||| updates the card with specified id
DELETE /cards/:id/	-	-	                    ||| deletes card with specified id
POST /cards/:id/image/ add a picture
POST /cards/:id/delete_image/ removes the picture
POST /cards/:id/like/ likes the card

GET	/users/	-	list of all people	
POST /users/:id/	user by id	user info       ||| add user as a friend
POST /users/:id/follow/     follows that user
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

    def retrieve(self, request, pk=None):
        queryset = (
            Card.objects.all()
            .select_related("user")
            .prefetch_related("liked_by", "comments")
        )
        card = get_object_or_404(queryset, pk=pk)
        serializer = CardSerializer(card, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def mine(self, request):
        cards = (
            Card.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("liked_by", "comments")
            .order_by("-posted_at")
        )
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def all(self, request):
        cards = (
            Card.objects.all()
            .select_related("user")
            .prefetch_related("liked_by", "comments")
            .order_by("-posted_at")
        )
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False)
    def following(self, request):
        cards = (
            Card.objects.filter(user__followers=self.request.user)
            .select_related("user")
            .prefetch_related("liked_by", "comments")
            .order_by("-posted_at")
        )
        serializer = CardSerializer(cards, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def image(self, request, pk, format=None):
        if "file" not in request.data:
            raise ParseError("Empty content")

        file = request.data["file"]
        card = self.get_object()

        card.image.save(file.name, file, save=True)
        return Response(status=201)

    @action(detail=True, methods=["POST"])
    def delete_image(self, request, pk, format=None):
        queryset = Card.objects.all()
        card = get_object_or_404(queryset, pk=pk)
        card.image.delete(save=True)
        return Response(status=204)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        card = self.get_object()
        card.liked_by.add(self.request.user)
        card.save()
        return Response(status=201)

    def get_parser_classes(self):
        print(self.action)
        if self.action == "image":
            return [FileUploadParser]

        return [JSONParser]

    def get_queryset(self):
        return (
            Card.objects.all()
            .select_related("user")
            .prefetch_related("liked_by", "comments")
            .order_by("-posted_at")
        )

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
        return (
            Comment.objects.all()
            .select_related("user", "card")
            .prefetch_related("liked_by")
        )

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
        return User.objects.all().prefetch_related("cards", "comments", "followers")

    @action(detail=True, methods=["GET"])
    def followers(self, request, pk):
        followers = self.get_object().followers.all()
        serializer = UserDisplaySerializer(
            followers, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["GET"])
    def following(self, request, pk):
        queryset = User.objects.all()
        person = get_object_or_404(queryset, pk=pk)
        following = User.objects.filter(followers=person)
        serializer = UserDisplaySerializer(
            following, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def follow(self, request, pk):
        person = self.get_object()
        person.followers.add(self.request.user)
        serializer = UserSerializer(person, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request, pk):
        person = self.get_object()
        person.followers.remove(self.request.user)
        person.save()
        # serializer = UserSerializer(person, context={"request": request})
        # return Response(serializer.data)
        return Response(status=204)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all().prefetch_related("cards", "comments", "followers")
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={"request": request})
        return Response(serializer.data)