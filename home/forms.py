from django import forms
from .models import Expense, Income
from decimal import Decimal, InvalidOperation

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'category', 'amount', 'date']

    def clean_amount(self) -> Decimal:
        """
        Validate the amount field.

        Returns:
            Decimal: The validated amount.

        Raises:
            forms.ValidationError: If the amount is invalid.
        """
        amount = self.cleaned_data.get('amount')
        try:
            amount = Decimal(str(amount).replace(',', '.'))
        except InvalidOperation:
            raise forms.ValidationError('Некоректне значення суми. Воно повинно бути числом з десятковою точкою.')

        if amount <= 0:
            raise forms.ValidationError("Сума повинна бути більшою за нуль.")

        if len(str(amount).replace('.', '').replace('-', '')) > 10:
            raise forms.ValidationError("Сума не повинна перевищувати 10 символів.")

        return amount

    def clean(self) -> dict:
        """
        Validate all fields.

        Returns:
            dict: The cleaned data.

        Raises:
            forms.ValidationError: If any field is invalid.
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')

        if not name or not category or not amount or not date:
            raise forms.ValidationError("Всі поля є обов'язковими для заповнення.")

        return cleaned_data

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'source', 'amount', 'date']

    def clean_amount(self) -> Decimal:
        """
        Validate the amount field.

        Returns:
            Decimal: The validated amount.

        Raises:
            forms.ValidationError: If the amount is invalid.
        """
        amount = self.cleaned_data.get('amount')
        try:
            amount = Decimal(str(amount).replace(',', '.'))
        except InvalidOperation:
            raise forms.ValidationError('Некоректне значення суми. Воно повинно бути числом з десятковою точкою.')

        if amount <= 0:
            raise forms.ValidationError("Сума повинна бути більшою за нуль.")

        if len(str(amount).replace('.', '').replace('-', '')) > 10:
            raise forms.ValidationError("Сума не повинна перевищувати 10 символів.")

        return amount

    def clean(self) -> dict:
        """
        Validate all fields.

        Returns:
            dict: The cleaned data.

        Raises:
            forms.ValidationError: If any field is invalid.
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        source = cleaned_data.get('source')
        amount = cleaned_data.get('amount')
        date = cleaned_data.get('date')

        if not name or not source or not amount or not date:
            raise forms.ValidationError("Всі поля є обов'язковими для заповнення.")

        return cleaned_data
