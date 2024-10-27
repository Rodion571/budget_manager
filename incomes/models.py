from django.db import models

class Income(models.Model):
    name = models.CharField(max_length=255)  # Убедитесь, что это поле присутствует
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
