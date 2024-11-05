from django.db import models


class Income(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)  # добавляем поле source
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.source} - {self.amount}'
