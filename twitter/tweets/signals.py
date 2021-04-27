from django.db.models.signals import post_save
from tweets.models import Tweet

#reciever
from django.dispatch import receiver

@receiver(post_save, sender=Tweet)
def create_thumbnail(sender, instance, created, **kwargs):
    if created:
        try:
            extension_list = instance.media.url.split('.')
            if extension_list[1] == "mp4":
                instance.is_video = True
        except:
            print("Not a video")
