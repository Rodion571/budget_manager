# expenses/models.py
from django.db import models

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description} - {self.amount}"

    class Meta:
        managed = True