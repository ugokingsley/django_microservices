from rest_framework import serializers, validators
from . models import *

class TransactionSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Transaction
        fields = '__all__'