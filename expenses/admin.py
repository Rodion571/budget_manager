from django.contrib import admin
from expenses.models import Expense

class ExpenseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Expense model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
    """
    list_display: tuple = ('name', 'amount', 'date', 'source')

admin.site.register(Expense, ExpenseAdmin)
