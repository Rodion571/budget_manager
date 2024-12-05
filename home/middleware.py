from django.shortcuts import redirect

class CheckAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in ['/accounts/login/', '/accounts/register/']:
            return redirect(f'/accounts/login/?next={request.path}')
        response = self.get_response(request)
        return response
