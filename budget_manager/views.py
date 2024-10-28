from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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


@login_required
def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})

@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def expense_chart(request):
    expenses = Expense.objects.all()
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='blue')
    plt.xlabel('Категорії')
    plt.ylabel('Сума')
    plt.title('Распределение расходов по категориям')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'expense_chart.html', {'graphic': graphic})

@login_required
def budget_planning(request):
    return render(request, 'budget_planning.html')

@login_required
def financial_tips(request):
    return render(request, 'financial_tips.html')

