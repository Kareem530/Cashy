from rest_framework import serializers
from accounts.api.serializers import UserSerializer
from transactions.models import UserTransaction, CashTransaction

class UserTransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = UserTransaction
        fields = "__all__"


class CashTransactionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CashTransaction
        fields = "__all__"