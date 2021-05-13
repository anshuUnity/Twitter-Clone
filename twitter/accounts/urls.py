from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.loginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('follow/', views.followUser, name='follow'),
    path('users/tweet/', views.ProfileUserTweet.as_view(), name='user_tweet'),
    path('tweets/liked/', views.ProfileUserLikedTweet.as_view(), name="liked_tweet"),
    path('user/reports/', views.render_pdf_view, name='user_report'),
    path('user/verify-email/', views.send_otp, name='email_verify'),
    path('enter-otp', views.check_otp, name='check_otp'),
]