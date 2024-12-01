from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the AbstractUser model.

    Attributes:
        email (models.EmailField): The email field for the custom user model.
    """
    email: models.EmailField = models.EmailField(unique=True)
