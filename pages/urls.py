from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='Home'),
    path("About", views.about, name='About'),
    path("Services", views.services, name='Services'),
]