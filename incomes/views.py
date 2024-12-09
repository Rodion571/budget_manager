from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Income
from .forms import IncomeForm

@login_required
def add_income(request: HttpRequest) -> HttpResponse:
    """
    Handle the addition of a new income.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered add income page.
    """
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'incomes/add_income.html', {'form': form})

@login_required
def income_list(request: HttpRequest) -> HttpResponse:
    """
    Render the income list and handle new income creation.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered income list page.
    """
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')  # Обновлено: убрано пространство имен
    else:
        form = IncomeForm()
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'form': form, 'incomes': incomes})
