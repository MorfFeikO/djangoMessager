from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile
from registration.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance)
        user_profile.save()
