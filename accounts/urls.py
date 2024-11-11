from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from . import views
from .views import register, user_login, user_logout, home

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
]
