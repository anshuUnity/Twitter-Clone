from django.contrib import admin

from tweets.models import Tweet, TweetComments
# Register your models here.

admin.site.register(Tweet)
admin.site.register(TweetComments)