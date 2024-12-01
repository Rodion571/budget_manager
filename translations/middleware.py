# translations/middleware.py
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class UserLanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = request.session.get('language')
        if language:
            translation.activate(language)
        else:
            translation.deactivate()
