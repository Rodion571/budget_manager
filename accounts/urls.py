from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns: list[path] = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home_content'),
    path('signup/', views.register, name='signup'),
]
