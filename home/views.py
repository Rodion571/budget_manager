from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
from incomes.models import Income
from expenses.forms import ExpenseForm
from incomes.forms import IncomeForm
import datetime
import matplotlib.pyplot as plt
import io
import base64

def home(request):
    return render(request, 'home.html')
def home_content(request):
    return render(request, 'home_content.html')
def profile(request):
    return render(request, 'profile.html')
@login_required
def income_list(request):
    if request.method == 'POST' and 'source' in request.POST:
        name = request.POST['name']
        source = request.POST['source']
        amount = request.POST['amount']
        Income.objects.create(name=name, source=source, amount=amount)
        return redirect('income_list')
    elif request.method == 'POST' and 'delete_income' in request.POST:
        income_id = request.POST['delete_income']
        Income.objects.filter(id=income_id).delete()
        return redirect('income_list')
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})

@login_required
def delete_income(request, id):
    income = get_object_or_404(Income, id=id)
    income.delete()
    return redirect('income_list')


@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

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
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'expense_chart.html', {'graphic': graphic})

@login_required
def budget_planning(request):
    return render(request, 'budget_planning.html')

@login_required
def financial_tips(request):
    return render(request, 'financial_tips.html')
