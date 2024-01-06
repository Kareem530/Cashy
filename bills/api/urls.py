from django.urls import path
from bills.api.views import PayBillsAPIView,PaidSearch

urlpatterns = [
    path("Paybills", PayBillsAPIView.as_view(), name='Paybills'),
    path("PaidSearch", PaidSearch.as_view(), name='PaidSearch'),
]