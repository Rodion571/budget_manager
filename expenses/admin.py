# expenses/admin.py
from django.contrib import admin
from expenses.models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date', 'category')  # замените name на существующие поля

admin.site.register(Expense, ExpenseAdmin)
