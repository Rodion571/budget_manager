# Generated by Django 5.1.2 on 2024-10-24 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
