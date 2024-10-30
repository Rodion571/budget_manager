"""
URL configuration for budget_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from budget_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('income-list/', views.income_list, name='income_list'),
    path('expense-list/', views.expense_list, name='expense_list'),
    path('expense-chart/', views.expense_chart, name='expense_chart'),
    path('budget-planning/', views.budget_planning, name='budget_planning'),
    path('financial-tips/', views.financial_tips, name='financial_tips'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('delete-income/<int:id>/', views.delete_income, name='delete_income'),
    path('add-income/', views.add_income, name='add_income'),

    path('accounts/', include('django.contrib.auth.urls')),  # Включим маршруты аутентификации
]



