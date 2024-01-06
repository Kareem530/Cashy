from django.db import models
from accounts.models import User

class BillCompany(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    earnings = models.IntegerField(default=0)
    

class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(BillCompany, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    