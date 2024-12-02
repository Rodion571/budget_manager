from django.contrib import admin
from incomes.models import Income

class IncomeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Income model.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
    """
    list_display: tuple = ('name', 'amount', 'date')

admin.site.register(Income, IncomeAdmin)
