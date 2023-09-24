from django.urls import path
from .views import *

urlpatterns = [
    path('pay/', payment, name='payment'),
    path('transaction/', view_transaction, name='view_transaction'),
    path('webhook/<str:transaction_ref>/', webhook_check, name='webhook_check'),
]
