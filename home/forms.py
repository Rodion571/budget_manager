from django import forms
from .models import Expense, Income

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'category', 'amount', 'date']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сума має бути більшою за нуль.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')

        if not name or not category or not amount or not date:
            raise forms.ValidationError("Всі поля є обов'язковими для заповнення.")

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'source', 'amount', 'date']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сума має бути більшою за нуль.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        source = cleaned_data.get('source')
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')

        if not name or not source or not amount or not date:
            raise forms.ValidationError("Всі поля є обов'язковими для заповнення.")
