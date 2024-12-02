from django import forms
from expenses.models import Expense
import datetime

class ExpenseForm(forms.ModelForm):
    """
    Form for creating and updating Expense instances.

    Attributes:
        model (Type[Expense]): The model associated with the form.
        fields (List[str]): The fields to include in the form.
    """
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'date']

    def clean_amount(self):
        """
        Validate that the amount is a positive number.

        Raises:
            forms.ValidationError: If the amount is not positive.
        """
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Сума повинна бути позитивним числом.')
        return amount

    def clean_date(self):
        """
        Validate that the date is not in the future.

        Raises:
            forms.ValidationError: If the date is in the future.
        """
        date = self.cleaned_data.get('date')
        if date > datetime.date.today():
            raise forms.ValidationError('Дата не може бути в майбутньому.')
        return date
