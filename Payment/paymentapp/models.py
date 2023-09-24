from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class UserToken(models.Model):
    user_id = models.CharField(blank=True, null=True, max_length=140)
    user_email = models.CharField(blank=True, null=True, max_length=140)
    user_token = models.CharField(blank=True, null=True, max_length=140)
        
    def __str__(self):
        return str(self.user_email)
                
    class Meta:
        ordering = ["-pk"]

class Transaction(models.Model):
    user_email = models.CharField(blank=True, null=True, max_length=140)
    transaction_ref = models.CharField(max_length=140, blank=True, null=True)
    amount = models.DecimalField(max_digits=50, default=0, decimal_places=1)
    narration = models.CharField(max_length=140, blank=True, null=True)

    def __str__(self):
        return str(self.user_email)
                
    class Meta:
        ordering = ["-pk"]
