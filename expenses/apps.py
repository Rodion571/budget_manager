from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    """
    Configuration for the expenses' application.

    Attributes:
        default_auto_field (str): The type of auto field to use for primary keys.
        name (str): The name of the application.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'expenses'
