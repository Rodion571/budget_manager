from django.shortcuts import render
from expenses.models import Expense
from incomes.models import Income


def home(request):
    expenses = Expense.objects.all()  # Получаем все расходы
    incomes = Income.objects.all()      # Получаем все доходы
    return render(request, 'home.html', {'expenses': expenses, 'incomes': incomes})
