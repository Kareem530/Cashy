from django.urls import path
from . import views

urlpatterns = [

    path("Login", views.login, name='Login'),
    path("Register", views.register, name='Register'),
    path("Logout", views.logout, name='Logout'),
    path("Dashboard", views.dashboard, name='Dashboard'),
    path("Cash_History", views.Cash_History, name='Cash_History'),
    path("Sent_History", views.Sent_History, name='Sent_History'),
    path("Received_History", views.Received_History, name='Received_History'),
    path("Paid_History", views.Paid_History, name='Paid_History'),
]