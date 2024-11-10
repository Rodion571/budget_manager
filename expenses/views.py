import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404

from expenses.models import Expense
from incomes.models import Income

from expenses.forms import ExpenseForm

from .models import Expense
from incomes.forms import IncomeForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    return render(request, 'home.html', {'expenses': expenses, 'incomes': incomes})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense

@login_required
def add_expense(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        date = request.POST['date']
        Expense.objects.create(name=name, amount=amount, date=date)
        return redirect('expenses:expense_list')
    return render(request, 'add_expense.html')

@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('home')

@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'incomes/../incomes/add_income.html', {'form': form})



@login_required
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

    return render(request, 'expenses/expense_chart.html', {'graphic': graphic})
