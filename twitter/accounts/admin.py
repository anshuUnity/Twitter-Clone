from django.contrib import admin
from accounts.models import Userprofile, Followers
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(Followers)