from django.urls import path

from . import views

urlpatterns = [
    path('Contact', views.contact, name='Contact')
]