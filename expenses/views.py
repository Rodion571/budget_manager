import io
import base64
import random
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from incomes.models import Income
from expenses.models import Expense
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
def expense_list(request: HttpRequest) -> HttpResponse:
    """
    Handle displaying and adding expenses.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response with the rendered expense list page.
    """
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'form': form, 'expenses': expenses})


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
    return redirect('expense_list')


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
    return render(request, 'incomes/add_income.html', {'form': form})


@login_required
def expense_chart(request: HttpRequest) -> HttpResponse:
    """
    Render a bar chart of expenses by source for a selected month.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered expense chart page.
    """
    if 'month' in request.GET:
        selected_month = request.GET['month']
    else:
        selected_month = datetime.datetime.now().strftime('%Y-%m')

    year, month = map(int, selected_month.split('-'))
    expenses = Expense.objects.filter(date__year=year, date__month=month)

    unique_sources = set(expense.source for expense in expenses)
    random.seed(42)
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_sources))
    source_color_map = {source: color for source, color in zip(unique_sources, colors)}

    for expense in expenses:
        expense.color = source_color_map[expense.source]

    source_totals = expenses.values('source').annotate(total=Sum('amount')).order_by('source')
    plt.figure(figsize=(10, 5))
    plt.bar([item['source'] for item in source_totals], [item['total'] for item in source_totals],
            color=[source_color_map[item['source']] for item in source_totals])
    plt.xlabel('Джерела', fontsize=14, fontweight='bold')
    plt.ylabel('Сума', fontsize=14, fontweight='bold')
    plt.title('Розподіл витрат по джерелах', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    ukr_months = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }
    month_name = f"{ukr_months[month]} {year}"

    return render(request, 'expense_chart.html', {'expenses': expenses, 'month': selected_month, 'month_name': month_name, 'graphic': graphic})


@login_required
def add_expense(request: HttpRequest) -> HttpResponse:
    """
    Handle adding a new expense.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered add expense page.
    """
    if request.method == 'POST':
        name = request.POST['name']
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']

        if not name or not source or not amount or not date:
            raise ValidationError("All fields are required.")

        Expense.objects.create(name=name, source=source, amount=amount, date=date)
        return redirect('expense_list')
    return render(request, 'expenses/add_expense.html')


@login_required
def home_content_view(request: HttpRequest) -> HttpResponse:
    """
    Render the home content view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered home content view.
    """
    expenses = Expense.objects.all()
    return render(request, 'home_content.html', {'expenses': expenses})
