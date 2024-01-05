from django.urls import path
from . import views

urlpatterns = [
    path("Paybills", views.Paybills, name='Paybills'),
    path("PaidSearch", views.PaidSearch, name='PaidSearch'),
]