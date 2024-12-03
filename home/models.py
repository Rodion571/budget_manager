from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation


class Budget(models.Model):
    """
    Model representing a budget.

    Attributes:
        name (str): The name of the budget.
        category (str): The category of the budget.
        amount (Decimal): The amount of the budget.
        date (datetime.date): The date the budget was created.
    """
    name: models.CharField = models.CharField(max_length=100, default='Бюджет')
    category: models.CharField = models.CharField(max_length=100)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    date: models.DateField = models.DateField()

    def __str__(self) -> str:
        """
        Return a string representation of the budget.

        Returns:
            str: The string representation of the budget.
        """
        return f"{self.name} - {self.category}: {self.amount:.2f} on {self.date}"


class Expense(models.Model):
    """
    Model representing an expense.

    Attributes:
        name (str): The name of the expense.
        source (str): The source of the expense.
        amount (Decimal): The amount of the expense.
        date (datetime.date): The date the expense was made.
    """
    name: models.CharField = models.CharField(max_length=100)
    source: models.CharField = models.CharField(max_length=100)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    date: models.DateField = models.DateField()

    def clean(self) -> None:
        """
        Validate the amount field.

        Raises:
            ValidationError: If the amount is invalid.
        """
        try:
            self.amount = Decimal(str(self.amount).replace(',', '.'))
        except InvalidOperation:
            raise ValidationError('Некоректне значення суми. Воно повинно бути числом з десятковою точкою.')

        if self.amount <= 0:
            raise ValidationError('Сума повинна бути більшою за нуль.')

        if len(str(self.amount).replace('.', '').replace('-', '')) > 10:
            raise ValidationError("Сума не повинна перевищувати 10 символів.")

    def __str__(self) -> str:
        """
        Return a string representation of the expense.

        Returns:
            str: The string representation of the expense.
        """
        return f"{self.name} - {self.source}: {self.amount:.2f} on {self.date}"


class Income(models.Model):
    """
    Model representing an income.

    Attributes:
        name (str): The name of the income.
        source (str): The source of the income.
        amount (Decimal): The amount of the income.
        date (datetime.date): The date the income was received.
        budget (Budget): The budget to which the income belongs.
    """
    name: models.CharField = models.CharField(max_length=100)
    source: models.CharField = models.CharField(max_length=100)
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    date: models.DateField = models.DateField()
    budget: models.ForeignKey = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='incomes')

    def clean(self) -> None:
        """
        Validate the amount field.

        Raises:
            ValidationError: If the amount is invalid.
        """
        try:
            self.amount = Decimal(str(self.amount).replace(',', '.'))
        except InvalidOperation:
            raise ValidationError('Некоректне значення суми. Воно повинно бути числом з десятковою точкою.')

        if self.amount <= 0:
            raise ValidationError('Сума повинна бути більшою за нуль.')

        if len(str(self.amount).replace('.', '').replace('-', '')) > 10:
            raise ValidationError("Сума не повинна перевищувати 10 символів.")

    def __str__(self) -> str:
        """
        Return a string representation of the income.

        Returns:
            str: The string representation of the income.
        """
        return f"{self.name} - {self.source}: {self.amount:.2f} on {self.date}"
