from django.db import models
from django.contrib.auth.models import AbstractUser

# Consider creating a custom user model from scratch as detailed at
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False
    )

    profile_picture = models.ImageField(upload_to="post_images/", null=True, blank=True)
