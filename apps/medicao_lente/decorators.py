from functools import wraps

from django.shortcuts import redirect


def autenticacao_necessaria(func):
    wraps(func)

    def wrapper(request, *args, **kwargs):
        if 'accessToken' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)

    return wrapper
