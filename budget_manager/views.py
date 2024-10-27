from django.shortcuts import render, redirect
from expenses.models import Expense
from incomes.models import Income
from expenses.forms import ExpenseForm
from incomes.forms import IncomeForm
import matplotlib.pyplot as plt
import io
import base64

def home(request):
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    return render(request, 'home.html', {'expenses': expenses, 'incomes': incomes})


def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'incomes/add_income.html', {'form': form})

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

    from django.shortcuts import get_object_or_404


    return render(request, 'expenses/expense_chart.html', {'graphic': graphic})
