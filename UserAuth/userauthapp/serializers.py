from rest_framework import serializers, validators
from django.contrib.auth.hashers import make_password
from . models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('username', 'email', 'password')

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators":[
                    validators.UniqueValidator(
                        User.objects.all(), "A user with this email exists"
                    )
                ]
            }
        }
        