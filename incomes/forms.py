# incomes/forms.py
from django import forms
from incomes.models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name','amount', 'source']  # Убедись, что поля совпадают с твоей моделью Income
