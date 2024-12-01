from django.urls import path
from . import views
from typing import List

app_name = 'new_app'

urlpatterns: List[path] = [
    path('', views.index, name='index'),
]
