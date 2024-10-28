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
from . import views
from budget_manager.views import home, budget_planning, financial_tips, income_list, expense_list, expense_chart, add_income, add_expense

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('expenses/', include('expenses.urls')),
    path('incomes/', include('incomes.urls')),
    path('budget-planning/', budget_planning, name='budget_planning'),
    path('financial-tips/', financial_tips, name='financial_tips'),
    path('income-list/', income_list, name='income_list'),
    path('expense-list/', expense_list, name='expense_list'),
    path('expense-chart/', expense_chart, name='expense_chart'),
    path('add-income/', add_income, name='add_income'),
    path('add-expense/', add_expense, name='add_expense'),
]



