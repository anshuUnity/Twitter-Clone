from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from .models import Tweet, TweetComments
from accounts.models import Userprofile
from django.contrib.auth.models import User
from django.views.generic import View
from .forms import TweetForm, CommentForm
from accounts.models import Followers
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomeView(View):

    def get(self, request):
        form = TweetForm()
        followObj = Followers.objects.get(user=request.user)
        following_obj = followObj.following.all()
        # tweet = Tweet.objects.all().order_by("-date")
        tweet = Tweet.objects.filter(user__in = following_obj).order_by("-date")
        context = {
            'tweet_form':form,
            'tweets':tweet,
        }
        return render(request, 'home.html', context)

    def post(self, request):
        if request.method == 'POST':
            form = TweetForm(request.POST, request.FILES)
            if form.is_valid():
                new_form = form.save(commit=False)
                user = request.user
                form.instance.user = user
                form.save()
                data = {}
                tweet_obg = Tweet.objects.get(id=form.instance.id)
                data = {
                    'tweet_content':tweet_obg.tweet_content,
                    'tweet_date':tweet_obg.date,
                    'tweet_user':tweet_obg.user.username,
                }
                if(tweet_obg.media):
                    data["tweet_media"] = str(tweet_obg.media.url)

                tweet = {"data":data}
                return JsonResponse(tweet)
            else:
                return JsonResponse({'error': True, 'errors': form.errors})


@csrf_exempt
def like_tweet(request):
    if request.method == 'POST':
        tweet_id = request.POST.get('tweet_id')
        tweet_obj = get_object_or_404(Tweet, id=tweet_id)
        liked = False
        if tweet_obj.likes.filter(id=request.user.id).exists():
            tweet_obj.likes.remove(request.user)
            liked = False

        else:
            tweet_obj.likes.add(request.user)
            liked = True
        like_count = tweet_obj.likes.count()
        data = {
            'liked':liked,
            'count':like_count,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'liked':'not worked'})

def tweetDetail(request, id):
    tweet_obj = get_object_or_404(Tweet, id=id)
    comment_obj = TweetComments.objects.filter(tweet=tweet_obj).order_by('-date')
    check_list = ['covid', 'vaccination', 'covid-19', 'covid19']
    covid_bar = False
    for i in check_list:
        if i in tweet_obj.tweet_content:
            covid_bar = True
            break
        else:
            pass

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            form.instance.user = request.user
            form.instance.tweet = tweet_obj
            form.save()
            form_data = {}
            comment_obj = TweetComments.objects.get(id=form.instance.id)
            data = {
                'comment':comment_obj.comment_content,
                'date':comment_obj.date,
                'name':comment_obj.user.userprofile.name,
                'comment_username':comment_obj.user.username,
                'tweet_username':tweet_obj.user.username,
            }
            if (comment_obj.user.userprofile.profileImage):
                data['comment_profile'] = str(comment_obj.user.userprofile.profileImage.url)
            else:
                data['comment_profile'] = str("https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640")
            return JsonResponse(data)
        else:
            return JsonResponse({"Error":form.errors})
    else:
        form = CommentForm()
        
    data = {
        'tweet':tweet_obj,
        'comments':comment_obj,
        'check_list': check_list,
        'covid_bar':covid_bar,
        'comment_form':form,
    }
    return render(request, 'tweets/tweet_detail.html', data)

