from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .models import Income

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
        name = request.POST['name']
        amount = request.POST['amount']
        date = request.POST['date']
        Income.objects.create(name=name, amount=amount, date=date)
        return redirect('incomes:income_list')
    return render(request, 'incomes/add_income.html')

@login_required
def income_list(request: HttpRequest) -> HttpResponse:
    """
    Render the income list page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered income list page.
    """
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})
