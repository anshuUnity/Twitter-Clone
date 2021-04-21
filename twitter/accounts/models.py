from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    coverImage = models.ImageField(null=True, blank=True)
    profileImage = models.ImageField(null=True, blank=True)
    bio = models.TextField(max_length=160, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    joining_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)


    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"username": self.user.username})
    

class Followers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    followers = models.ManyToManyField(User, related_name="followed_user", blank=True)

    def __str__(self):
        return str(self.user.username)

