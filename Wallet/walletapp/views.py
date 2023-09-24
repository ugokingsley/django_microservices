from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .models import *
from .producer import publish
from .serializers import *
import random


class UserWalletViewSet(viewsets.ViewSet):
    def list(self, request):
        userwallet = UserWallet.objects.all()
        serializer = UserWalletSerializer(userwallet, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_user_wallet(request):
    user = request.headers.get('Authorization').removeprefix('Token ')
    user_email = UserToken.objects.get(user_token=user).user_email  
    user_wallet = UserWallet.objects.get(user_email=user_email).account_balance
    wallet_details = {
        'user':user_email,
        'wallet_balance':user_wallet
    }  
    return Response(wallet_details)


@api_view(['GET', 'PUT'])
def user_wallet_update(request, email):
    try:
        user_wallet = UserWallet.objects.get(user_email=email)
        data = {
            'username':user_wallet.username,
            'user_email':user_wallet.user_email,
            'account_balance':user_wallet.account_balance
        }
    except UserWallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserWalletSerializer(user_wallet)
        return Response(data)

    elif request.method == 'PUT':
        serializer = UserWalletSerializer(user_wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)