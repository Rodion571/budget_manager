# Generated by Django 5.1.2 on 2024-11-05 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0004_alter_income_name_alter_income_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='income',
            name='source',
            field=models.CharField(max_length=255),
        ),
    ]