# translations/views.py
from django.utils import translation
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse


# noinspection PyTypeChecker
def set_language(request: HttpRequest) -> HttpResponse:
    """
    Set the user's preferred language and redirect to the previous page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object that redirects to the previous page.
    """
    user_language = request.GET.get('language', 'en')
    translation.activate(user_language)
    request.session['language'] = user_language
    return redirect(request.META.get('HTTP_REFERER'))
