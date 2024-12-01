from django.apps import AppConfig


class NewAppConfig(AppConfig):
    """
    Configuration for the new_app application.

    Attributes:
        default_auto_field (str): The type of auto field to use for primary keys.
        name (str): The name of the application.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'new_app'
