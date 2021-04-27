from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import re

from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()

@register.filter(name='linkerate')
@stringfilter
def linktruncate(value):
    return value[12:]

@register.filter(name='anshu')
@stringfilter
def lowers(value):
    at_rate_users_list = (re.findall(r'(?<=\W)[@]\S*', value))
    # making new list by removing @
    content_list = value.split()
    res= ''
    try:
        new_username_list = []
        for i in at_rate_users_list:
            new_username_list.append(i[1:])

        users = User.objects.filter(username__in = new_username_list).select_related('userprofile')
        # for user in users:
        #     print(user.userprofile.get_absolute_url())
        for i in content_list:
            if i[0] == '@':
                username_c = i[1:]
                for user in users:
                    if user.username == username_c:
                        profile_link = user.userprofile.get_absolute_url()
                        i = f"<a href='{profile_link}'>{i}</a>"
            
            res = res + i +' '
        return res
    except:
        print("Could not populate @")
