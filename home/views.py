from django.shortcuts import render, redirect, get_object_or_404
from expenses.models import Expense
from incomes.models import Income
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from expenses.forms import ExpenseForm
from .models import Budget
from incomes.forms import IncomeForm
import matplotlib.colors as mcolors
import random
import datetime
import matplotlib.pyplot as plt
import io
import base64
from django.contrib.auth import get_user_model
import logging
User = get_user_model()

# Ваша модель пользователя CustomUser используется через get_user_model()

def home(request):
    return render(request, 'home.html')
def home_content(request):
    return render(request, 'home_content.html')
@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')
def profile(request):
    return render(request, 'profile.html')
@login_required
def income_list(request):
    if request.method == 'POST' and 'source' in request.POST:
        name = request.POST['name']
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        Income.objects.create(name=name, source=source, amount=amount, date=date)
        return redirect('income_list')
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})


@login_required
def delete_income(request, id):
    income = get_object_or_404(Income, id=id)
    income.delete()
    return redirect('income_list')



logger = logging.getLogger(__name__)

@login_required
def add_expense(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        Budget.objects.create(name=name, category=category, amount=amount, date=date)
        return redirect('home:expense_list')
    return render(request, 'add_expense.html')

@login_required
def add_income(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        Budget.objects.create(name=name, category=category, amount=amount, date=date)
        return redirect('home:expense_list')
    return render(request, 'incomes/add_income.html')

@login_required
def budget_planning(request):
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
    return render(request, 'budget_planning.html', {'budgets': budgets, 'total_income': total_income, 'total_expense': total_expense, 'remaining_budget': remaining_budget})

@login_required
def delete_budget(request, id):
    budget = get_object_or_404(Budget, id=id)
    budget.delete()
    return redirect('budget_planning')

@login_required
def expense_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        amount = request.POST['amount']
        date = request.POST['date']
        Expense.objects.create(name=name, category=category, amount=amount, date=date)
        return redirect('expense_list')
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})


@login_required
def expense_chart(request):
    expenses = Expense.objects.all()
    categories = [expense.category for expense in expenses]
    amounts = [expense.amount for expense in expenses]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, amounts, color='blue')
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

    return render(request, 'expense_chart.html', {'graphic': graphic})

@login_required
def financial_tips(request):
    return render(request, 'financial_tips.html')

@login_required
def expense_chart(request):
    if 'month' in request.GET:
        selected_month = request.GET['month']
    else:
        selected_month = datetime.datetime.now().strftime('%Y-%m')

    year, month = map(int, selected_month.split('-'))
    expenses = Expense.objects.filter(date__year=year, date__month=month)

    # Генерируем цвета для категорий
    unique_categories = set(expense.category for expense in expenses)
    random.seed(42)  # для повторяемости
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_categories))
    category_color_map = {category: color for category, color in zip(unique_categories, colors)}

    for expense in expenses:
        expense.color = category_color_map[expense.category]  # Устанавливаем цвет категории

    # Создаем график расходов по категориям
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

    # Перевод названий месяцев на украинский
    ukr_months = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }
    month_name = f"{ukr_months[month]} {year}"

    return render(request, 'expense_chart.html',
                  {'expenses': expenses, 'month': selected_month, 'month_name': month_name, 'graphic': graphic})

@login_required
def income_chart(request):
    if 'month' in request.GET:
        selected_month = request.GET['month']
    else:
        selected_month = datetime.datetime.now().strftime('%Y-%m')

    year, month = map(int, selected_month.split('-'))
    incomes = Income.objects.filter(date__year=year, date__month=month)

    # Генерируем цвета для категорий доходов
    unique_sources = set(income.source for income in incomes)
    random.seed(42)  # для повторяемости
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_sources))
    source_color_map = {source: color for source, color in zip(unique_sources, colors)}

    for income in incomes:
        income.color = source_color_map[income.source]  # Устанавливаем цвет категории

    # Создаем график доходов по категориям
    source_totals = incomes.values('source').annotate(total=Sum('amount')).order_by('source')
    plt.figure(figsize=(10, 5))
    plt.bar([item['source'] for item in source_totals], [item['total'] for item in source_totals], color=[source_color_map[item['source']] for item in source_totals])
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

    # Перевод названий месяцев на украинский
    ukr_months = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }
    month_name = f"{ukr_months[month]} {year}"

    return render(request, 'income_chart.html', {'incomes': incomes, 'month': selected_month, 'month_name': month_name, 'graphic': graphic, 'type': 'income'})

@login_required
def expense_income_chart(request):
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

    # Генерируем цвета для категорий
    unique_categories = set(getattr(item, category_field) for item in items)
    random.seed(42)  # для повторяемости
    colors = random.sample(list(mcolors.CSS4_COLORS.values()), len(unique_categories))
    category_color_map = {category: color for category, color in zip(unique_categories, colors)}

    for item in items:
        setattr(item, 'color', category_color_map[getattr(item, category_field)])  # Устанавливаем цвет категории

    # Создаем график по категориям
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

    # Перевод названий месяцев на украинский
    ukr_months = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }
    month_name = f"{ukr_months[month]} {year}"

    return render(request, 'home.html',
                  {'items': items, 'month': selected_month, 'month_name': month_name, 'graphic': graphic,
                   'type': chart_type})

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

logger = logging.getLogger(__name__)

def signup(request):
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
    return render(request, 'registration.html', {'form': form})
