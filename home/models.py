from django.db import models

class Budget(models.Model):
    """
    Model representing a budget.

    Attributes:
        name (str): The name of the budget.
        category (str): The category of the budget.
        amount (Decimal): The amount allocated to the budget.
        date (datetime.date): The date the budget was created.
    """
    name: str = models.CharField(max_length=100, default='Бюджет')
    category: str = models.CharField(max_length=100)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    date: models.DateField = models.DateField()

    def __str__(self) -> str:
        """
        Return a string representation of the budget.

        Returns:
            str: The string representation of the budget.
        """
        return f"{self.name} - {self.category}: {self.amount:.2f} on {self.date}"
