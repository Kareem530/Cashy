from django.db import models
from accounts.models import User

class UserTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class CashType(models.TextChoices):
    DEPOSIT = 'Deposit'
    WITHDRAW = 'Withdraw'

class CashTransaction(models.Model):
    cash_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cash_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=8, choices=CashType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    