from django.db import models
from registration.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.user.username


class Message(models.Model):
    user = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.DO_NOTHING,
    )
    body = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message -> {self.user.username}-{self.created_at}"
