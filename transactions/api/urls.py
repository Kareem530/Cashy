from django.urls import path
from transactions.api.views import *

urlpatterns = [

    path("SendMoney", SendMoney.as_view(), name='SendMoney'),
    path("CashTransactions", CashTransactions.as_view(), name='CashTransactions'),
    path("CashSearch", CashSearch.as_view(), name='CashSearch'),
    path("SentSearch", SentSearch.as_view(), name='SentSearch'),
    path("ReceivedSearch", ReceivedSearch.as_view(), name='ReceivedSearch'),
    
]