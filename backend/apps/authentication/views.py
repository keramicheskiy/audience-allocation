from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.authentication.serializers import CustomUserSerializer
from .decorators import authenticated
from .models import CustomUser
from .tasks import send_mail
from .services import verify_email, notify_moderators


# Create your views here.


@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return Response({"fields": CustomUserSerializer.Meta.fields})

    elif request.method == 'POST':
        print("Получены данные:", request.data)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            verify_email(user)
            notify_moderators(user)

            response = Response({
                'token': token.key,
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

            return response
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({'error': 'missing user'}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': CustomUserSerializer(user).data})


@api_view(['GET'])
@authenticated
def verify_token(request):
    token = request.COOKIES.get('Token')
    user = Token.objects.get(key=token).user
    return Response({"user": user}, status=status.HTTP_200_OK)
