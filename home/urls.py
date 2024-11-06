from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_content, name='home_content'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-income/', views.add_income, name='add_income'),
    path('expense-list/', views.expense_list, name='expense_list'),
    path('budget-planning/', views.budget_planning, name='budget_planning'),
]
