from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from knox.auth import AuthToken
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from . serializers import *
from .producer import publish


@api_view(['POST'])
def register_api(request):
    data = request.data
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
           user = User.objects.create(
               username = data['username'],
               email = data['email'],
               password = make_password(data['password'])
           )
           _,token = AuthToken.objects.create(user)
           
           publish('user_created', serializer.data) 

           return Response({
                'message': 'User registered',
                'email': user.email,
                'token':token
                
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response({
                'error': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(serializer.errors)


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    user_details = {
        'id': user.id,
        'email': user.email,
        'token':token  }
    if token:
        publish('user_token', user_details)
        return Response(user_details)
    else:
        return Response({'error':'Cannot Log In'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_api(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'id': user.id,
            'email': user.email,
        })
    return Response({
        'error': 'Not Authenticated',
    }, status=status.HTTP_400_BAD_REQUEST)