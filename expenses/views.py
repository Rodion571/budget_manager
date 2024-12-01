import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from expenses.models import Expense
from incomes.models import Income

from expenses.forms import ExpenseForm
from incomes.forms import IncomeForm

@login_required
def home(request: HttpRequest) -> HttpResponse:
    """
    Render the home page with lists of expenses and incomes.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with rendered home page.
    """
    expenses = Expense.objects.all()
    incomes = Income.objects.all()
    return render(request, 'home.html', {'expenses': expenses, 'incomes': incomes})

@login_required
def add_expense(request: HttpRequest) -> HttpResponse:
    """
    Handle the addition of a new expense.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered add expense page.
    """
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        date = request.POST['date']
        Expense.objects.create(name=name, amount=amount, date=date)
        return redirect('expenses:expense_list')
    return render(request, 'add_expense.html')

@login_required
def expense_list(request: HttpRequest) -> HttpResponse:
    """
    Render the expense list page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered expense list page.
    """
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def delete_expense(request: HttpRequest, expense_id: int) -> HttpResponseRedirect:
    """
    Handle the deletion of an expense.

    Args:
        request (HttpRequest): The HTTP request object.
        expense_id (int): The ID of the expense to delete.

    Returns:
        HttpResponseRedirect: The HTTP response redirect object.
    """
    expense = get_object_or_404(Expense, id=expense_id)
    expense.delete()
    return redirect('home')

@login_required
def add_income(request: HttpRequest) -> HttpResponse:
    """
    Handle the addition of a new income.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered add income page.
    """
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'incomes/../incomes/add_income.html', {'form': form})

@login_required
def expense_chart(request: HttpRequest) -> HttpResponse:
    """
    Render a bar chart of expenses by category.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered expense chart page.
    """
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
