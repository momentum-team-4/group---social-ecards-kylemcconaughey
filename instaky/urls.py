from django.urls import include, path
from rest_framework import routers

from . import views as instaky_views

api_router = routers.DefaultRouter()


api_router.register("posts", instaky_views.PostViewSet, basename="post")
api_router.register("comments", instaky_views.CommentViewSet, basename="comment")
api_router.register("users", instaky_views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(api_router.urls)),
]