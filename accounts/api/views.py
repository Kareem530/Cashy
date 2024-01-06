from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
from accounts.api.serializers import UserSerializer
from transactions.api.serializers import CashTransactionSerializer,UserTransactionSerializer
from bills.api.serializers import BillSerializer
from bills.models import Bill
from transactions.models import CashTransaction,UserTransaction
from accounts.api.pagination import HistoryPagination


@api_view(['POST',])
def logout(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response("logout Successful",status=status.HTTP_200_OK)

@api_view(['POST',])
def register(request):

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['Response'] = "Registration Successful"
            data['First_Name'] = account.first_name
            data['Last_Name'] = account.last_name
            data['Username'] = account.username
            data['Email'] = account.email
            data['Phone_Number'] = account.phonenum

            token = Token.objects.get(user=account).key
            data['Token'] = token
            
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
    
class dashboard(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        data = {}
        
        Cash_Transactions = CashTransaction.objects.filter(user = request.user).order_by('-timestamp')[:5]
        Sent_Transactions = UserTransaction.objects.filter(sender = request.user).order_by('-timestamp')[:5]
        Received_Transactions = UserTransaction.objects.filter(receiver = request.user).order_by('-timestamp')[:5]
        Paid_Bills = Bill.objects.filter(sender = request.user).order_by('-timestamp')[:5]
        
        CashSerializer = CashTransactionSerializer(Cash_Transactions, many=True).data
        SentSerializer = UserTransactionSerializer(Sent_Transactions, many=True).data
        ReceivedSerializer = UserTransactionSerializer(Received_Transactions, many=True).data
        PaidBillsSerializer = BillSerializer(Paid_Bills, many=True).data
        
        cash_data = [{"Date": item["timestamp"], "Type": item["type"], "Amount": item["amount"]} for item in CashSerializer]
        sent_data = [{"Date": item["timestamp"],"Sender": item["sender"], "Receiver": item["receiver"], "Amount": item["amount"]} for item in SentSerializer]
        received_data = [{"Date": item["timestamp"], "Sender": item["sender"],"Receiver": item["receiver"], "Amount": item["amount"]} for item in ReceivedSerializer]
        paid_bills_data = [{"Date": item["timestamp"],"Sender": item["sender"], "Receiver": item["receiver"], "Amount": item["amount"]} for item in PaidBillsSerializer]
        Userdata = [{'First Name': request.user.first_name,'Last Name': request.user.last_name,'Username' : request.user.username, 'Email' : request.user.email,'Balance': request.user.balance}]
        
        data['User Info']=Userdata
        data['Cash_Transactions'] = cash_data
        data['Sent_Transactions'] = sent_data
        data['Received_Transactions'] = received_data
        data['Paid_Bills'] = paid_bills_data
        
        return Response(data, status=status.HTTP_200_OK)


class Cash_History(generics.ListAPIView):
    serializer_class = CashTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        return CashTransaction.objects.filter(user = self.request.user).order_by('-timestamp')
    
class Sent_History(generics.ListAPIView):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        return UserTransaction.objects.filter(sender = self.request.user).order_by('-timestamp')
    
class Received_History(generics.ListAPIView):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        return UserTransaction.objects.filter(receiver = self.request.user).order_by('-timestamp')
    
class Paid_History(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        return Bill.objects.filter(sender = self.request.user).order_by('-timestamp')