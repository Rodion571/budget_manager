from django.contrib import admin
from incomes.models import Income

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'date')  # Убедись, что здесь указаны правильные поля

admin.site.register(Income, IncomeAdmin)
