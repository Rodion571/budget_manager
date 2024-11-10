from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income

@login_required
def add_income(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        date = request.POST['date']
        Income.objects.create(name=name, amount=amount, date=date)
        return redirect('incomes:income_list')
    return render(request, 'incomes/add_income.html')

@login_required
def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'income_list.html', {'incomes': incomes})
