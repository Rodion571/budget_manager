# Generated by Django 5.1.2 on 2024-11-05 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='type',
            new_name='category',
        ),
        migrations.AddField(
            model_name='budget',
            name='name',
            field=models.CharField(default='Бюджет', max_length=100),
        ),
    ]