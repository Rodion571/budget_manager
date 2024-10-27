import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, redirect
from expenses.models import Expense
from incomes.models import Income
from expenses.forms import ExpenseForm  # Импортируем из правильного модуля
from incomes.forms import IncomeForm

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form':form})

def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

def expense_chart(request):
    expenses = Expense.objects.all()
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='blue')
    plt.xlabel('Категории')
    plt.ylabel('Сумма')
    plt.title('Распределение расходов по категориям')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'expense_chart.html', {'graphic': graphic})
