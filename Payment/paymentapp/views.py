from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.db.models import Avg, Min, Max, Count, Exists, OuterRef
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
import requests
import random


@api_view(['POST'])
def payment(request):
    try:
        with transaction.atomic():
            user = request.headers.get('Authorization').removeprefix('Token ')
            user_email = UserToken.objects.get(user_token=user).user_email
            get_wallet = requests.get('http://docker.for.mac.localhost:8002/api/wallet/v1/user_wallet/'+user_email+'/')
            data = get_wallet.json()
            current_balance = data['account_balance']
            amount = int(request.data['amount'])
            new_balance = current_balance+amount
            pay_wallet = requests.put('http://docker.for.mac.localhost:8002/api/wallet/v1/user_wallet/'+user_email+'/', data={'account_balance': new_balance})
            instance = Transaction(
                            user_email=user_email,
                            transaction_ref = str(random.randint(100000, 999999)),
                            amount = request.data['amount'],
                            narration = f"Transferred {request.data['amount']} to {user_email}",
                            status='success',
                    )
            instance.save()
            return Response({'message':'successful','account_balance':new_balance})
    except:
        #raise
        instance = Transaction(
                        user_email=user_email,
                        transaction_ref = str(random.randint(100000, 999999)),
                        amount = request.data['amount'],
                        narration = f"Transferred {request.data['amount']} to {user_email}",
                        status='failed',
            )
        instance.save()
        return Response({'error':'something went wrong, try again later'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_transaction(request):
    transaction = Transaction.objects.all()  
    serializer = TransactionSerializer(transaction, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def webhook_check(request,transaction_ref):
    try:
        transaction = Transaction.objects.get(transaction_ref=transaction_ref)
        data = {
            'user_email':transaction.user_email,
            'Reference':transaction.transaction_ref,
            'amount':transaction.amount,
            'narration':transaction.narration,
            'narration':transaction.status
        }
    except UserWallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(data)