from django.urls import path
from .views import add_income, income_list

urlpatterns = [
    path('add/', add_income, name='add_income'),
    path('list/', income_list, name='income_list'),
]
