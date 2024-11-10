from django.urls import path
from . import views

app_name = 'incomes'

urlpatterns = [
    path('add/', views.add_income, name='add_income'),
    path('list/', views.income_list, name='income_list'),
]
