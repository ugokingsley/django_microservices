from django.urls import path
from .views import *

urlpatterns = [
    path('user_wallet/', get_user_wallet, name='get_user_wallet'),
    path('wallet/', UserWalletViewSet.as_view({
        'get': 'list',
    })),
    path('user_wallet/<str:email>/', user_wallet_update, name='user_wallet_update'),
]
