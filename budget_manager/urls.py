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
from home import views

urlpatterns = [
    # Основные страницы
    path('', views.home_content, name='home_content'),
    path('home/', views.home, name='home'),
    path('income-list/', views.income_list, name='income_list'),
    path('expense-list/', views.expense_list, name='expense_list'),
    path('expense-chart/', views.expense_chart, name='expense_chart'),
    path('expense-income-chart/', views.expense_income_chart, name='expense_income_chart'),
    path('budget-planning/', views.budget_planning, name='budget_planning'),
    path('add-budget/', views.budget_planning, name='add_budget'),
    path('financial-tips/', views.financial_tips, name='financial_tips'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('profile/', views.profile, name='profile'),
    path('delete-income/<int:id>/', views.delete_income, name='delete_income'),
    path('delete-expense/<int:id>/', views.delete_expense, name='delete_expense'),
    path('income-chart/', views.income_chart, name='income_chart'),
    path('signup/', views.signup, name='signup'),
    path('delete-budget/<int:id>/', views.delete_budget, name='delete_budget'),

    # Включение других URL конфигураций
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('home/', include(('home.urls', 'home'), namespace='home')),
    path('new_app/', include(('new_app.urls', 'new_app'), namespace='new_app')),
    path('expenses/', include(('expenses.urls', 'expenses'), namespace='expenses')),
    path('incomes/', include(('incomes.urls', 'incomes'), namespace='incomes')),

    # Административная часть
    path('admin/', admin.site.urls),
]
