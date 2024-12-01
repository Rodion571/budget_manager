from django import forms
from incomes.models import Income

class IncomeForm(forms.ModelForm):
    """
    Form for creating and updating Income instances.

    Attributes:
        model (Type[Income]): The model associated with the form.
        fields (List[str]): The fields to include in the form.
    """
    class Meta:
        model: type = Income
        fields: list[str] = ['name', 'amount', 'source']
