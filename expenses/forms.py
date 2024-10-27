# expenses/forms.py
from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date']  # Убедись, что поля совпадают с твоей моделью Expense
