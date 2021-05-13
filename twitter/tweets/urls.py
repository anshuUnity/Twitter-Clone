from django.urls import path
from tweets import views

app_name = 'tweets'

urlpatterns = [
    path('liked/', views.like_tweet, name='liked'),
    path('tweet/<int:id>/', views.tweetDetail, name='tweet_detail'),
    path('search/', views.get_ajax_search_result, name='search'),
]