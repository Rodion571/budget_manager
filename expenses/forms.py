from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    """
    Form for creating and updating Expense instances.

    Attributes:
        model (Type[Expense]): The model associated with the form.
        fields (List[str]): The fields to include in the form.
    """
    class Meta:
        model: type = Expense
        fields: list[str] = ['amount', 'category', 'date']
