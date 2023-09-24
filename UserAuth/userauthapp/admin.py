from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email', 'date_created']

admin.site.register(User, UserAdmin)