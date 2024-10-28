from django.shortcuts import render, redirect, get_object_or_404
from incomes.models import Income
from .forms import IncomeForm
from django.contrib.auth.decorators import login_required

@login_required
def income_list(request):
    incomes = Income.objects.all()
    return render(request, 'incomes/income_list.html', {'incomes': incomes})

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')  # предполагается, что такой URL будет создан
    else:
        form = IncomeForm()
    return render(request, 'incomes/add_income.html', {'form': form})
