from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.api.views import *


urlpatterns = [

    path("Login", obtain_auth_token, name='Login'),
    path("Register", register, name='Register'),
    path("Logout", logout, name='Logout'),
    path("Dashboard", dashboard.as_view(), name='Dashboard'),
    path("Cash_History", Cash_History.as_view(), name='Cash_History'),
    path("Sent_History", Sent_History.as_view(), name='Sent_History'),
    path("Received_History", Received_History.as_view(), name='Received_History'),
    path("Paid_History", Paid_History.as_view(), name='Paid_History'),
]