from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('login/', views.loginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('follow/', views.followUser, name='follow'),
]