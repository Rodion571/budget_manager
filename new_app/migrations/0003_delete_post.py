# Generated by Django 5.1.2 on 2024-12-01 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0002_remove_post_updated_at_alter_post_created_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
