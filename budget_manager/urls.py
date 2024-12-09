from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from accounts import views as accounts_views
from expenses import views as expenses_views
from incomes import views as incomes_views
from new_app import views as new_app_views

urlpatterns = [
    # URLs для home
    path('', home_views.home_content, name='home_content'),
    path('home/', home_views.home, name='home'),
    path('income-list/', home_views.income_list, name='income_list'),
    path('expense-list/', expenses_views.expense_list, name='expense_list'),
    path('expense-chart/', expenses_views.expense_chart, name='expense_chart'),
    path('expense-income-chart/', home_views.expense_income_chart, name='expense_income_chart'),
    path('budget-planning/', home_views.budget_planning, name='budget_planning'),
    path('add-budget/', home_views.budget_planning, name='add_budget'),
    path('financial-tips/', home_views.financial_tips, name='financial_tips'),
    path('add-expense/', expenses_views.add_expense, name='add_expense'),
    path('profile/', home_views.profile, name='profile'),
    path('delete-income/<int:id>/', home_views.delete_income, name='delete_income'),
    path('delete-expense/<int:id>/', expenses_views.delete_expense, name='delete_expense'),
    path('income-chart/', home_views.income_chart, name='income_chart'),
    path('signup/', home_views.signup, name='signup'),
    path('delete-budget/<int:id>/', home_views.delete_budget, name='delete_budget'),
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.user_login, name='login'),
    # URLs для accounts
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),  # Добавлено пространство имен и include

    # URLs для expenses
    path('expenses/add/', expenses_views.add_expense, name='add_expense'),
    path('expenses/chart/', expenses_views.expense_chart, name='expense_chart'),
    path('expenses/delete/<int:expense_id>/', expenses_views.delete_expense, name='delete_expense'),
    path('expenses/list/', expenses_views.expense_list, name='expense_list'),
    path('expenses/home_content/', expenses_views.home_content_view, name='home_content'),

    # URLs для incomes
    path('incomes/add/', incomes_views.add_income, name='add_income'),
    path('incomes/list/', incomes_views.income_list, name='income_list'),

    # URLs для new_app
    path('new_app/', new_app_views.index, name='index'),


    # Admin URL
    path('admin/', admin.site.urls),

]
