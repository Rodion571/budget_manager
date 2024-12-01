from django.apps import AppConfig


class LocalesConfig(AppConfig):
    """
    Configuration for the locales application.

    Attributes:
        default_auto_field (str): The type of auto field to use for primary keys.
        name (str): The name of the application.
    """
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'locales'
