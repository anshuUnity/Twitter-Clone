from django.shortcuts import render, get_object_or_404, Http404
from .forms import SignUpForm, UserProfileForm

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import View

from django.db.models import Count

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# my models
from .models import Followers, Userprofile
from tweets.models import Tweet

from django.contrib.auth import get_user_model

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

import random
from django.conf import settings

from .tasks import send_mail_otp_task


User = get_user_model()

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save()
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
    user = get_object_or_404(User.objects.select_related('userprofile', 'followers'), username=username)
    profile = user.userprofile
    profile_form = UserProfileForm(instance=profile)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                update = form.save(commit=False)
                update.user=user
                update.save()
            return HttpResponseRedirect(profile.get_absolute_url())
        else:
            form = UserProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'profile':user, 'p_form':profile_form})

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

class ProfileUserTweet(View):
    def get(self, request):
        profile_username = request.GET.get('username')
        user_data = User.objects.select_related('userprofile').get(username=profile_username)
        user_tweet = list(Tweet.objects.filter(user__username=profile_username).values())
        data = {
            'user_tweet':user_tweet,
            'username': user_data.username,
        }
        if user_data.userprofile.name:
            data['fullname'] = user_data.userprofile.name
        if user_data.userprofile.is_verified:
            data['is_verified'] = True
        else:
            data['is_verified'] = False

        if user_data.userprofile.profileImage:
            data['profile_pic'] = str(user_data.userprofile.profileImage.url)
        else:
            data['profile_pic'] = "https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640"

        return JsonResponse(data, safe=False)

class ProfileUserLikedTweet(View):
    def get(self, request):
        profile_username = request.GET.get('username')
        user_data = User.objects.select_related('userprofile').get(username=profile_username)
        liked_post = Tweet.objects.filter(likes=user_data).select_related('user')

        if liked_post:
            query_list = []

            for item in liked_post:
                query_dict = {
                    'username': item.user.username,
                    'content': item.tweet_content,
                    'fullname':item.user.userprofile.name,
                }

                if item.user.userprofile.profileImage:
                    query_dict['profile_pic'] = str(item.user.userprofile.profileImage.url)
                else:
                    query_dict['profile_pic'] = "https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640"

                query_list.append(query_dict)
                data = {
                    'is_data':True,
                    'liked_post':query_list
                }
        else:
            message = f"<b>@{user_data.username}</b> has not liked any tweet, When they do, it will appear here."
            data = {
                'is_data': False,
                'liked_post': message
            }

        return JsonResponse(data, safe=False)


def render_pdf_view(request):

    if request.user.is_authenticated:
        profile_user = User.objects.select_related('userprofile').prefetch_related('tweet_set').get(username=request.user.username)
        total_likes = profile_user.tweet_set.aggregate(total_likes=Count('likes'))['total_likes'] or 0

    template_path = 'accounts/user_report.html'
    context = {'p_user': profile_user, 'total_likes':total_likes}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if download is required
        # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    # only display
    response['Content-Disposition'] = f'filename="{request.user.username}.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        otp = random.randint(1000, 9999)
        request.session['email_otp'] = otp
        subject = "Verify Your Email"
        message = f'Your OTP for email verification is {otp}, remember that this otp will expire after 10 minutes'
        email_from = settings.EMAIL_HOST_USER
        recepient_list = [request.user.email]
        try:
            send_mail_otp_task.delay(subject, message, email_from, recepient_list)
            return JsonResponse({'data':'OTP Send Successfully'})
        except:
            print('Mail Not Send')
            return JsonResponse({'data':'Error sending mail'})
    else:
        return HttpResponseRedirect(reverse('home'))

@csrf_exempt
def check_otp(request):
    if request.method == 'POST':
        u_otp = request.POST.get('u_otp', False)
        otp = request.session['email_otp']
        if int(u_otp) == otp:
            curr_user_profile = Userprofile.objects.get(user=request.user)
            curr_user_profile.mail_verified = True
            curr_user_profile.save()
            return JsonResponse({'data': True})
        else:
            return JsonResponse({'error': True})
    return HttpResponseRedirect(reverse('home'))

@login_required
def editprofile(request):
    user = User.objects.get(username=request.user.username)
    print(user.username)
    return HttpResponse(user.username)