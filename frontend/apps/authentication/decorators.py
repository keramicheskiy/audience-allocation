from functools import wraps

import requests
from django.shortcuts import redirect

from apps.authentication.serializers import CustomUserSerializer
from frontend.settings import BACKEND_URL


def approved_role(func):
    @wraps(func)
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
            if CustomUserSerializer(response.json())['role'] == 'none':
                return redirect('/profile')
        except requests.RequestException:
            return redirect('/auth/login')

        return func(request, *args, **kwargs)

    return wrapper
