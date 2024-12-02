from django.db import models

class Income(models.Model):
    """
    Model representing an income.

    Attributes:
        name (str): The name of the income.
        amount (Decimal): The amount of the income.
        date (datetime.date): The date of the income.
    """
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


    def __str__(self) -> str:
        return f"{self.name}: {self.amount} on {self.date}"
