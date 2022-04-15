from django.db import models

from registration.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        User,
        related_name="user_follows",
        symmetrical=False,
        blank=True,
    )
    followers = models.ManyToManyField(
        User,
        related_name="users_followers",
        symmetrical=False,
        blank=True,
    )

    def is_follow(self, other_user):
        if other_user in self.follows.all():
            return True
        return False

    def __str__(self):
        return self.user.username


class Message(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.DO_NOTHING,
    )
    body = models.CharField(max_length=100)
    liked_by = models.ManyToManyField(
        User,
        related_name="liked",
        symmetrical=False,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def is_liked_by(self, user):
        if user in self.liked_by.all():
            return True
        return False

    def __str__(self):
        return f"Message -> {self.owner.username}-{self.created_at}"
