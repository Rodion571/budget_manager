# translations/middleware.py
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest


class UserLanguageMiddleware(MiddlewareMixin):
    """
    Middleware to activate/deactivate the user's preferred language based on the session.

    Methods:
        process_request(request): Activates or deactivates the user's preferred language.
    """

    def process_request(self, request: HttpRequest) -> None:
        """
        Activates or deactivates the user's preferred language based on the session.

        Args:
            request (HttpRequest): The HTTP request object.
        """
        language = request.session.get('language')
        if language:
            translation.activate(language)
        else:
            translation.deactivate()
