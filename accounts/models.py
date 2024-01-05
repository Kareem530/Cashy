from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phonenum = models.CharField(max_length=50, unique=True)
    balance = models.IntegerField(default=0)
