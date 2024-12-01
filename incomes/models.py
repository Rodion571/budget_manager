from django.db import models

class Income(models.Model):
    """
    Model representing an income.

    Attributes:
        date (datetime.date): The date of the income.
        name (str): The name of the income.
        source (str): The source of the income.
        amount (Decimal): The amount of the income.
    """
    date: models.DateField = models.DateField()
    name: models.CharField = models.CharField(max_length=255)
    source: models.CharField = models.CharField(max_length=255)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        """
        Return a string representation of the income.

        Returns:
            str: The string representation of the income.
        """
        return f'{self.source} - {self.amount}'
