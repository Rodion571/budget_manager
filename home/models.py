from django.db import models

class Budget(models.Model):
    name = models.CharField(max_length=100, default='Бюджет')  # Название бюджета
    category = models.CharField(max_length=100)  # Категория (Доход или Витрати)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма
    date = models.DateField()  # Дата

    def __str__(self):
        return f"{self.name} - {self.category}: {self.amount} on {self.date}"
