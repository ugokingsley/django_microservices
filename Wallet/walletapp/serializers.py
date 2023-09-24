from rest_framework import serializers, validators
from . models import *


class UserWalletSerializer(serializers.ModelSerializer):
    account_balance = serializers.DecimalField(max_digits=16, decimal_places=2)
    class Meta:
        model = UserWallet
        #fields = '__all__'
        fields = ['username','user_email','account_balance']
