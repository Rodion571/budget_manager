# Generated by Django 5.1.2 on 2024-12-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0005_alter_income_name_alter_income_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='income',
            name='source',
        ),
        migrations.AlterField(
            model_name='income',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]