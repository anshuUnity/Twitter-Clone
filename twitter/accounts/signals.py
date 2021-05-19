from django.db.models.signals import post_save
from django.contrib.auth.models import User

#reciever
from django.dispatch import receiver
from .models import Userprofile, Followers

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)
        Followers.objects.create(user=instance)