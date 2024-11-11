from django.urls import path

from incomes.urls import app_name
from .views import register, user_login, user_logout, home

app_name = 'accounts'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home_content'),
]
