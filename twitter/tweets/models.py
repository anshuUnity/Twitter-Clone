from django.db import models
from django.contrib.auth.models import User
import uuid
import os
from moviepy.editor import *
# Create your models here.

# commanda if migrations not working
# python manage.py migrate <app_name> zero
# delete all initial file 
# python manage.py makemigrations
# python manage.py migrate

class Tweet(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tweet_key = models.UUIDField(default=uuid.uuid4, max_length=40, unique=True, editable=False)
    tweet_content = models.TextField(max_length=240, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='tweet-media', blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='tweet_likes')
    is_video = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}-{self.tweet_key}"

class TweetComments(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(to=Tweet, on_delete=models.CASCADE)
    comment_content = models.TextField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    comment_media = models.ImageField(upload_to='comment-media', blank=True, null=True)
    comment_likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    def __str__(self):
        return f"{self.user.username} reply to {self.tweet.tweet_key}"

