from django.urls import path
from . import views
from typing import List

app_name = 'incomes'

urlpatterns: List[path] = [
    path('add/', views.add_income, name='add_income'),
    path('list/', views.income_list, name='income_list'),
]
