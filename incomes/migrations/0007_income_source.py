# Generated by Django 5.1.2 on 2024-12-02 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomes', '0006_remove_income_source_alter_income_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='source',
            field=models.CharField(default='default_source', max_length=255),
            preserve_default=False,
        ),
    ]