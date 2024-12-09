from django import forms
from .models import Income


class IncomeForm(forms.ModelForm):
    """
    Form for the Income model, used for validation and cleaning of income data.
    """

    class Meta:
        model: Income = Income
        fields: list[str] = ['name', 'source', 'amount', 'date']

    def clean_amount(self) -> float:
        """
        Method to clean and validate the 'amount' field.

        Returns:
            float: Validated 'amount' value.

        Raises:
            forms.ValidationError: If the amount is less than or equal to zero.
        """
        amount: float = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сума має бути більшою за нуль.")
        return amount

    def clean(self) -> dict:
        """
        Method for overall cleaning and validation of all form fields.

        Returns:
            dict: Cleaned form data.

        Raises:
            forms.ValidationError: If any of the required fields are not filled.
        """
        cleaned_data: dict = super().clean()
        name: str = cleaned_data.get('name')
        source: str = cleaned_data.get('source')
        amount: float = cleaned_data.get('amount')
        date: str = cleaned_data.get('date')

        if not name or not source or not amount or not date:
            raise forms.ValidationError("Всі поля є обов'язковими для заповнення.")
        return cleaned_data
