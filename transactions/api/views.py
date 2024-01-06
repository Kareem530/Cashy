import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from django.shortcuts import get_object_or_404
from transactions.models import CashTransaction,UserTransaction
from .serializers import CashTransactionSerializer, UserTransactionSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
import requests
from accounts.api.pagination import HistoryPagination

class CashTransactions(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        type = request.data.get('type')
        amount = request.data.get('amount')
    
        if float(amount) <= 0:
            return Response({'Error': 'Amount must be greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if type not in ["Deposit", "Withdraw"]:
            return Response({'Error': 'Invalid transaction type.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        if type == "Deposit":
            serializer = CashTransactionSerializer(data=request.data)
            if serializer.is_valid():
             serializer.save(user=user)
             user.balance += float(amount)
             user.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
             return Response(serializer.errors)
        
        if type == "Withdraw" and float(amount) <= float(user.balance):
            serializer = CashTransactionSerializer(data=request.data)
            if serializer.is_valid():
             serializer.save(user=user)
             user.balance -= float(amount)
             user.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
             return Response(serializer.errors)
        else:
            return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)
  
class SendMoney(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_Username = request.data.get('recipient_Username')
        recipient_phone = request.data.get('recipient_phone')
        amount = request.data.get('amount')
        receiver = get_object_or_404(User, username=recipient_Username)

        if not recipient_Username or not recipient_phone or not amount:
            return Response({'error': 'Recipient Username, Phone Number and amount are required fields.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(username=recipient_Username).exists():
            return Response({'error': 'This User Does Not Exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.username == recipient_Username:
            return Response({'error': 'Cannot transfer to self.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not User.objects.filter(phonenum=recipient_phone).exists():
            return Response({'error': 'This Phone Number Does Not Exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if recipient_phone != receiver.phonenum:
            return Response({'error': 'Phone number does not match the recipient.'}, status=status.HTTP_400_BAD_REQUEST)

        if float(amount) <= 0:
            return Response({'error': 'Amount must be valid and greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)

        sender = request.user
        
        if float(amount) <= float(sender.balance):
            
            serializer = UserTransactionSerializer(data=request.data)
            if serializer.is_valid():
             serializer.save(sender=sender,receiver=receiver)
             sender.balance -= float(amount)
             sender.save()
             receiver.balance += float(amount)
             receiver.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
             return Response(serializer.errors)
         
        return Response({'error': 'Insufficient funds.'}, status=status.HTTP_400_BAD_REQUEST)

class CashSearch(generics.ListAPIView):
    serializer_class = CashTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = CashTransaction.objects.filter(user=self.request.user).order_by('-timestamp')
        
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        
        return queryset

class SentSearch(generics.ListAPIView):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = UserTransaction.objects.filter(sender=self.request.user).order_by('-timestamp')
        
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        
        return queryset

class ReceivedSearch(generics.ListAPIView):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = UserTransaction.objects.filter(receiver=self.request.user).order_by('-timestamp')
        
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        
        return queryset




           

