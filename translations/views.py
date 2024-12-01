# translations/views.py
from django.utils import translation
from django.shortcuts import redirect

def set_language(request):
    user_language = request.GET.get('language', 'en')
    translation.activate(user_language)
    request.session['language'] = user_language  # Обновлено для использования ключа 'language'
    return redirect(request.META.get('HTTP_REFERER'))
