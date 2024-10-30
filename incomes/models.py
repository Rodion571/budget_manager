from django.db import models

class Income(models.Model):
    name = models.CharField(max_length=100)  # Добавлено поле name
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # Дата присваивается автоматически
