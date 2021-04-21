from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()

@register.filter(name='linkerate')
@stringfilter
def linktruncate(value):
    return value[12:]


@register.filter(name='anshu', is_safe=True)
@stringfilter
def lowers(value):
    res = ""
    my_list = value.split()
    for i in my_list:
        # if i[0] == '#':
        #     i = f"<span style=color:#0000EE;>{i}</span>"
        #     i = f"<a style='text-decoration:none;' href = '#'>{i}</a>"

        if i[0] == '@':
            try:
                stng = i[1:]
                user = User.objects.get(username = stng)
                if user:
                    profile_link = user.userprofile.get_absolute_url()
                    # i = f"<span style=color:#0000EE;>{i}</span>"
                    i = f"<a href='{profile_link}'>{i}</a>"

            except User.DoesNotExist:
                print("Could not get the data")

        res = res + i + ' '
        
    return res