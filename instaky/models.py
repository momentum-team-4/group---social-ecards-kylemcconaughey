from django.db import models
from users.models import User
from datetime import timedelta


class Post(models.Model):
    outer_text = models.CharField(max_length=255, null=False, blank=False)

    inner_text = models.CharField(max_length=255, null=False, blank=False)

    posted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")

    is_public = models.BooleanField(null=False, blank=False, default=True)

    CARD_COLOR_CHOICES = [
        (0, "White"),
        (1, "Red"),
        (2, "Orange"),
        (3, "Yellow"),
        (4, "Green"),
        (5, "Blue"),
        (6, "Indigo"),
        (7, "Violet"),
        (8, "Black"),
    ]

    card_color = models.CharField(
        max_length=1,
        choices=CARD_COLOR_CHOICES,
        default=0,
    )

    BORDER_STYLE_CHOICES = [
        (0, "tbd"),
        (1, "tbd"),
        (2, "etc"),
    ]

    border_style = models.CharField(
        max_length=1,
        choices=BORDER_STYLE_CHOICES,
        default=0,
    )

    FONT_STYLE_CHOICES = [
        (0, "Comic Sans"),
        (1, "Papyrus"),
        (2, "Wingdings"),
    ]

    font_style = models.CharField(
        max_length=1,
        choices=FONT_STYLE_CHOICES,
        default=0,
    )

    TEXT_ALIGN_CHOICES = [
        (0, "Left"),
        (1, "Right"),
        (2, "Center"),
        (3, "Justified"),
    ]

    text_align = models.CharField(
        max_length=1,
        choices=TEXT_ALIGN_CHOICES,
        default=0,
    )

    FONT_SIZE_CHOICES = [
        (0, "Small"),
        (1, "Medium"),
        (2, "Large"),
        (3, "XXXtra Large"),
    ]

    font_size = models.CharField(
        max_length=1,
        choices=FONT_SIZE_CHOICES,
        default=0,
    )

    # image = models.FileField()

    def nicePosted(self):
        nice_posted = self.posted_at - timedelta(hours=4)
        return nice_posted.strftime("%A, %b %d at %I:%M %p")

    favorited_by = models.ManyToManyField(
        to=User, related_name="favorited_posts", blank=True
    )

    def isFavorited(self):
        if self.user in self.user.starred_questions.all():
            return True
        return False

    def __str__(self):
        return f"{self.inner_text}"


class Comment(models.Model):
    body = models.CharField(max_length=255, blank=False, null=False)

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")

    posted_at = models.DateTimeField(auto_now_add=True)

    favorited_by = models.ManyToManyField(
        to=User, related_name="favorited_comments", blank=True
    )

    def nicePosted(self):
        nice_posted = self.posted_at - timedelta(hours=4)
        return nice_posted.strftime("%A, %b %d at %I:%M %p")

    def __str__(self):
        return f"{self.body}"