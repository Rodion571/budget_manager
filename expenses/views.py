# expenses/views.py
from django.shortcuts import render, redirect
from expenses.models import Expense
from .forms import ExpenseForm

# Отображение списка расходов
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

# Добавление нового расхода
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # предполагается, что такой URL будет создан
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})
