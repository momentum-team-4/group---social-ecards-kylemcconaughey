from django.db import models
from users.models import User


class Card(models.Model):
    outer_text = models.CharField(max_length=255, null=False, blank=False)

    inner_text = models.CharField(max_length=255, null=False, blank=False)

    posted_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="cards")

    is_public = models.BooleanField(null=False, blank=False, default=True)

    class CardColorChoices(models.TextChoices):
        WHITE = "WH", ("White")
        BLACK = "BL", ("Black")
        RED = "RD", ("Red")
        ORANGE = "OR", ("Orange")
        YELLOW = "YE", ("Yellow")
        GREEN = "GR", ("Green")
        BLUE = "BL", ("Blue")
        INDIGO = "IN", ("Indigo")
        VIOLET = "VI", ("Violet")
        TEAL = "TE", ("Teal")

    card_color = models.CharField(
        max_length=2,
        choices=CardColorChoices.choices,
        default=CardColorChoices.WHITE,
    )

    class BorderStyleChoices(models.IntegerChoices):
        SOLID = 0, ("Solid")
        DASHED = 1, ("Dashed")
        DOTTED = 2, ("Dotted")
        DOUBLE = 3, ("Double")

    border_style = models.CharField(
        max_length=1,
        choices=BorderStyleChoices.choices,
        default=BorderStyleChoices.SOLID,
    )

    class FontFamilyChoices(models.CharField):
        SERIF = "SE", ("Serif")
        SANSERIF = "SS", ("Sans-Serif")

    font_family = models.CharField(
        max_length=2,
        choices=FontFamilyChoices.choices,
        default=FontFamilyChoices.SANSERIF,
    )

    class FontStyleChoices(models.CharField):
        ITALICS = "I", ("Italics")
        BOLD = "B", ("Bold")
        UNDERLINE = "U", ("Underline")

    font_style = models.CharField(
        max_length=1, choices=FontStyleChoices.choices, default=FontStyleChoices.ITALICS
    )

    class TextAlignChoices(models.CharField):
        LEFT = "L", ("Left")
        RIGHT = "R", ("Right")
        CENTER = "C", ("Center")
        JUSTIFIED = (
            "J",
            ("Justified"),
        )

    text_align = models.CharField(
        max_length=1,
        choices=TextAlignChoices.choices,
        default=TextAlignChoices.LEFT,
    )

    class FontSizeChoices(models.IntegerChoices):
        SMALL = (
            "0",
            ("Small"),
        )
        MEDIUM = (
            "1",
            ("Medium"),
        )
        LARGE = (
            "2",
            ("Large"),
        )
        XLARGE = (
            "3",
            ("Xtra Large"),
        )

    font_size = models.IntegerChoices(
        max_length=1,
        choices=FontSizeChoices.choices,
        default=FontSizeChoices.MEDIUM,
    )

    # image = models.FileField()

    favorited_by = models.ManyToManyField(
        to=User, related_name="favorited_cards", blank=True
    )

    def __str__(self):
        return f"{self.id}"
        # this needs to change, maybe? idk how we should specify which card to link comments to


class Comment(models.Model):
    body = models.CharField(max_length=255, blank=False, null=False)

    card = models.ForeignKey(to=Card, on_delete=models.CASCADE, related_name="comments")

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")

    posted_at = models.DateTimeField(auto_now_add=True)

    favorited_by = models.ManyToManyField(
        to=User, related_name="favorited_comments", blank=True
    )

    def __str__(self):
        return f"{self.body}"
