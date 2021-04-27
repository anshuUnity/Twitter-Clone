from django.shortcuts import render, get_object_or_404, Http404
from accounts.forms import SignUpForm

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# my models
from accounts.models import Followers, Userprofile

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            print("THANKS")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return HttpResponseRedirect(reverse('home'))
    
    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form':form})

def loginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account Not Active")
        else:
            context = {'notfound':True}
            print(f"NO ACCOUNT FOUND WITH USERNAME {username} AND PASSWORD {password}")
            print(context)
            return render(request, 'accounts/login.html',context)

    else:
        return render(request, 'accounts/login.html')

def profile_detail(request, username):
    profile = get_object_or_404(User.objects.select_related('userprofile', 'followers'), username=username)
    return render(request, 'accounts/profile.html', {'profile':profile})

@csrf_exempt
@login_required
def followUser(request):
    if request.method == 'POST':
        profile_pk = request.POST.get('profile_pk')
        profile_user = User.objects.get(id=profile_pk)
        follower_obj_profile_user = Followers.objects.get(user=profile_user)
        follower_obj_current_user = Followers.objects.get(user=request.user)
        follow=False

        if profile_user in follower_obj_current_user.following.all():
            follower_obj_current_user.following.remove(profile_user)
            follower_obj_profile_user.followers.remove(request.user)
            follow = False
        else:
            follower_obj_current_user.following.add(profile_user)
            follower_obj_profile_user.followers.add(request.user)
            follow = True
        followers_count = follower_obj_profile_user.followers.count()
        following_count = follower_obj_profile_user.following.count()

        data = {
            'follow':follow,
            'followers_count': followers_count,
            'following_count': following_count,
        }

        return JsonResponse(data)
    
    return HttpResponseRedirect(reverse('home'))

