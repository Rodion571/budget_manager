from django.urls import path
from .views import register, user_login, user_logout, home, set_language
from django.contrib import admin
from django.http import HttpResponse
from typing import List

app_name = 'accounts'

urlpatterns: List[path] = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home_content'),
    path('admin/', admin.site.urls),
    path('set_language/', set_language, name='set_language'),
]
