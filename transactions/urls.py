from django.urls import path
from . import views

urlpatterns = [

    path("SendMoney", views.SendMoney, name='SendMoney'),
    path("CashTransactions", views.CashTransactions, name='CashTransactions'),
    path("CashSearch", views.CashSearch, name='CashSearch'),
    path("SentSearch", views.SentSearch, name='SentSearch'),
    path("ReceivedSearch", views.ReceivedSearch, name='ReceivedSearch'),
    
]