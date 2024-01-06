from rest_framework import serializers
from accounts.api.serializers import UserSerializer
from bills.models import Bill, BillCompany

class BillCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BillCompany
        exclude = ('is_active','company_id')
        


class BillSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.company_name', read_only=True)

    class Meta:
        model = Bill
        fields = "__all__"