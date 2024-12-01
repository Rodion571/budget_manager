from django.urls import path
from .views import set_language
from typing import List

urlpatterns: List[path] = [
    path('set-language/', set_language, name='set_language'),
]
