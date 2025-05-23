from functools import wraps
import requests
from django.http import HttpResponse
from django.shortcuts import redirect
from apps.authentication.serializers import CustomUserSerializer
from frontend.settings import BACKEND_URL, permitted_roles


def role_required(required_role):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            token = request.COOKIES.get('token')
            if not token:
                return redirect('/auth/login')
            try:
                response = requests.get(
                    url=BACKEND_URL + "/auth/verify-token",
                    headers={'Authorization': f'Token {token}'}
                )
                if response.status_code != 200:
                    return redirect('/auth/login')
                user = CustomUserSerializer(response.json()).data
                if user["role"] in permitted_roles(required_role):
                    return func(request, *args, **kwargs)
                return redirect('/errors/wrong_role') # TODO СДЕЛАТЬ ПРИЛОЖЕНИЕ errors
            except requests.RequestException:
                return HttpResponse(status=504)

        return wrapper

    return decorator
