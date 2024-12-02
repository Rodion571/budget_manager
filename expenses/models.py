from django.db import models

class Expense(models.Model):
    """
    Model representing an expense.

    Attributes:
        name (str): The name of the expense.
        category (str): The category of the expense.
        amount (Decimal): The amount of the expense.
        date (datetime.date): The date of the expense.
    """
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.name} - {self.category}: {self.amount} on {self.date}"

