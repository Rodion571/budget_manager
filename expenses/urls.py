from django.urls import path
from .views import add_expense, expense_chart, expense_list, delete_expense

urlpatterns = [
    path('add/', add_expense, name='add_expense'),
    path('chart/', expense_chart, name='expense_chart'),
    path('delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('list/', expense_list, name='expense_list')

]
