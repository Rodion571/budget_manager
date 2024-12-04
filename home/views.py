import matplotlib.pyplot as plt
import io
import base64
import logging
import datetime
import random
import matplotlib.colors as mcolors
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from expenses.models import Expense
from incomes.models import Income
from .models import Budget
from incomes.forms import IncomeForm
from .forms import ExpenseForm
User = get_user_model()
logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    """Render the home page."""
    return render(request, 'home.html')

def home_content(request: HttpRequest) -> HttpResponse:
    """Render the home content page."""
    return render(request, 'home_content.html')

from django.shortcuts import redirect, get_object_or_404
from .models import Expense
from django.contrib.auth.decorators import login_required

@login_required
def delete_expense(request, id):
    """
    Handle deleting an expense.

    Args:
        request (HttpRequest): The HTTP request.
        id (int): The ID of the expense to delete.

    Returns:
        HttpResponse: The HTTP response redirecting to the expense list page.
    """
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')

def profile(request: HttpRequest) -> HttpResponse:
    """Render the profile page."""
    return render(request, 'profile.html')

@login_required
def income_list(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
        else:
            return render(request, 'income_list.html', {'form': form, 'incomes': Income.objects.all()})
    else:
        form = IncomeForm()

    return render(request, 'income_list.html', {'form': form, 'incomes': Income.objects.all()})


@login_required
def delete_income(request: HttpRequest, id: int) -> HttpResponseRedirect:
    """Handle the deletion of an income."""
    income = get_object_or_404(Income, id=id)
    income.delete()
    return redirect('income_list')

@login_required
def add_expense(request: HttpRequest) -> HttpResponse:
    """
    Handle adding a new expense.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: The HTTP response with the rendered add expense page.
    """
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']

        if not name or not category or not amount or not date:
            raise ValidationError("All fields are required.")

        Expense.objects.create(name=name, source=category, amount=amount, date=date)
        return redirect('expense_list')
    return render(request, 'expenses/add_expense.html')

@login_required
def add_income(request: HttpRequest) -> HttpResponse:
    """Handle the addition of a new income."""
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']

        if not name or not category or not amount or not date:
            raise ValidationError("Всі поля обов'язкові для заповнення.")

        Income.objects.create(name=name, category=category, amount=amount, date=date)
        return redirect('income_list')
    return render(request, 'incomes/add_income.html')


@login_required
def budget_planning(request: HttpRequest) -> HttpResponse:
    """Handle budget planning and display current budgets."""
    if request.method == 'POST':
        if 'delete_budget' in request.POST:
            budget_id = request.POST['delete_budget']
            budget = get_object_or_404(Budget, id=budget_id)
            budget.delete()
        else:
            name = request.POST['name']
            category = request.POST['category']
            amount = request.POST['amount']
            date = request.POST['date']
            Budget.objects.create(name=name, category=category, amount=amount, date=date)
        return redirect('budget_planning')
    budgets = Budget.objects.all()
    total_income = sum(budget.amount for budget in budgets if budget.category == 'Доход')
    total_expense = sum(budget.amount for budget in budgets if budget.category == 'Витрати')
    remaining_budget = total_income - total_expense
    return render(request, 'budget_planning.html', {
        'budgets': budgets,
        'total_income': total_income,
        'total_expense': total_expense,
        'remaining_budget': remaining_budget
    })

@login_required
def delete_budget(request: HttpRequest, id: int) -> HttpResponseRedirect:
    """Handle the deletion of a budget."""
    budget = get_object_or_404(Budget, id=id)
    budget.delete()
    return redirect('budget_planning')

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
            return render(request, 'expense_list.html', {'form': form, 'expenses': Expense.objects.all()})
    else:
        form = ExpenseForm()

    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'form': form, 'expenses': expenses})

@login_required
def expense_chart(request: HttpRequest) -> HttpResponse:
    """Render a bar chart of expenses by category for a selected month."""
    if 'month' in request.GET:
        selected_month = request.GET['month']
    else:
        selected_month = datetime.datetime.now().strftime('%Y-%m')

    year, month = map(int, selected_month.split('-'))
    expenses = Expense.objects.filter(date__year=year, date__month=month)

    unique_categories = set(expense.category for expense in expenses)
    random.seed(42)
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_categories))
    category_color_map = {category: color for category, color in zip(unique_categories, colors)}

    for expense in expenses:
        expense.color = category_color_map[expense.category]

    category_totals = expenses.values('category').annotate(total=Sum('amount')).order_by('category')
    plt.figure(figsize=(10, 5))
    plt.bar([item['category'] for item in category_totals], [item['total'] for item in category_totals],
            color=[category_color_map[item['category']] for item in category_totals])
    plt.xlabel('Категорії', fontsize=14, fontweight='bold')
    plt.ylabel('Сума', fontsize=14, fontweight='bold')
    plt.title('Розподіл витрат по категоріях', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
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

    return render(request, 'expense_chart.html',
                  {'expenses': expenses, 'month': selected_month, 'month_name': month_name, 'graphic': graphic})

@login_required
def financial_tips(request: HttpRequest) -> HttpResponse:
    """Render the financial tips page."""
    return render(request, 'financial_tips.html')


@login_required
def expense_chart(request: HttpRequest) -> HttpResponse:
    """
    Render a bar chart of expenses by category for a selected month.

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

    unique_categories = set(expense.category for expense in expenses)
    random.seed(42)
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_categories))
    category_color_map = {category: color for category, color in zip(unique_categories, colors)}

    for expense in expenses:
        expense.color = category_color_map[expense.category]

    category_totals = expenses.values('category').annotate(total=Sum('amount')).order_by('category')
    plt.figure(figsize=(10, 5))
    plt.bar([item['category'] for item in category_totals], [item['total'] for item in category_totals],
            color=[category_color_map[item['category']] for item in category_totals])
    plt.xlabel('Категорії', fontsize=14, fontweight='bold')
    plt.ylabel('Сума', fontsize=14, fontweight='bold')
    plt.title('Розподіл витрат по категоріях', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
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
def income_chart(request: HttpRequest) -> HttpResponse:
    """
    Render a bar chart of incomes by source for a selected month.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered income chart page.
    """
    if 'month' in request.GET:
        selected_month = request.GET['month']
    else:
        selected_month = datetime.datetime.now().strftime('%Y-%m')

    year, month = map(int, selected_month.split('-'))
    incomes = Income.objects.filter(date__year=year, date__month=month)

    unique_sources = set(income.source for income in incomes)
    random.seed(42)
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_sources))
    source_color_map = {source: color for source, color in zip(unique_sources, colors)}

    for income in incomes:
        income.color = source_color_map[income.source]

    source_totals = incomes.values('source').annotate(total=Sum('amount')).order_by('source')
    plt.figure(figsize=(10, 5))
    plt.bar([item['source'] for item in source_totals], [item['total'] for item in source_totals],
            color=[source_color_map[item['source']] for item in source_totals])
    plt.xlabel('Джерела доходу', fontsize=14, fontweight='bold')
    plt.ylabel('Сума', fontsize=14, fontweight='bold')
    plt.title('Розподіл доходів по джерелах', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
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

    return render(request, 'income_chart.html', {'incomes': incomes, 'month': selected_month, 'month_name': month_name, 'graphic': graphic, 'type': 'income'})

@login_required
def expense_income_chart(request: HttpRequest) -> HttpResponse:
    """
    Render a bar chart of expenses or incomes by category for a selected month based on the chart type.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered expense or income chart page.
    """
    if 'month' in request.GET:
        selected_month = request.GET['month']
    else:
        selected_month = datetime.datetime.now().strftime('%Y-%m')

    if 'type' in request.GET:
        chart_type = request.GET['type']
    else:
        chart_type = 'expenses'

    year, month = map(int, selected_month.split('-'))

    if chart_type == 'expenses':
        items = Expense.objects.filter(date__year=year, date__month=month)
        category_field = 'category'
    else:
        items = Income.objects.filter(date__year=year, date__month=month)
        category_field = 'source'

    unique_categories = set(getattr(item, category_field) for item in items)
    random.seed(42)
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_categories))
    category_color_map = {category: color for category, color in zip(unique_categories, colors)}

    for item in items:
        setattr(item, 'color', category_color_map[getattr(item, category_field)])  # Устанавливаем цвет категории

    category_totals = items.values(category_field).annotate(total=Sum('amount')).order_by(category_field)
    plt.figure(figsize=(10, 5))
    plt.bar([item[category_field] for item in category_totals], [item['total'] for item in category_totals],
            color=[category_color_map[item[category_field]] for item in category_totals])
    plt.xlabel('Категорії', fontsize=14, fontweight='bold')
    plt.ylabel('Сума', fontsize=14, fontweight='bold')
    plt.title('Розподіл по категоріях', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
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

    return render(request, 'home.html', {'items': items, 'month': selected_month, 'month_name': month_name, 'graphic': graphic, 'type': chart_type})


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating a new user with email.

    Attributes:
        email (forms.EmailField): The email field for the user creation form.
    """
    email: forms.EmailField = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Save the user with the provided email.

        Args:
            commit (bool): Whether to commit the changes to the database.

        Returns:
            User: The saved user instance.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

import logging

logger = logging.getLogger(__name__)

def signup(request: HttpRequest) -> HttpResponse:
    """
    Handle user signup.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered signup page.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_content')
            else:
                logger.error(f'Authentication failed for user: {username}')
                form.add_error(None, 'Ошибка аутентификации.')
        else:
            logger.error('Form is invalid')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
