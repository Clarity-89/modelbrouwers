from django.db.models.signals import post_save
from django.dispatch import receiver

from general.models import UserProfile
from .models import User


@receiver(post_save, sender=User)
def create_userprofile(sender, **kwargs):
    if kwargs.get('created'):
        user = kwargs.get('instance')
        fields = {
            'user': user,
            'forum_nickname': user.username,
        }
        UserProfile.objects.create(**fields)
