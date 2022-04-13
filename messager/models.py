from django.db import models
from django.http import Http404
from registration.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="user_follows",
        symmetrical=False,
        blank=True,
    )
    followers = models.ManyToManyField(
        "self",
        related_name="users_followers",
        symmetrical=False,
        blank=True,
    )

    @classmethod
    def current_profile(cls, user):
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            raise Http404

    @classmethod
    def other_profile(cls, pk):
        try:
            return cls.objects.get(id=pk)
        except cls.DoesNotExist:
            raise Http404

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
