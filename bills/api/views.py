from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from django.shortcuts import get_object_or_404
from bills.models import BillCompany, Bill
from .serializers import BillSerializer,BillCompanySerializer
from rest_framework.permissions import IsAuthenticated
from accounts.api.pagination import HistoryPagination

class PayBillsAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bill_companies = BillCompany.objects.filter(is_active=True)
        serializer = BillCompanySerializer(bill_companies,many=True)
        return Response(serializer.data)

    def post(self, request):
        bill_company = request.data.get('bill_company')
        amount = request.data.get('amount')

        if not bill_company or not amount:
            return Response({'error': 'Bill company and amount are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        if float(amount) <= 0:
            return Response({'error': 'Amount must be valid and greater than 0.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        bill_receiver = get_object_or_404(BillCompany, company_name=bill_company)
        
        if float(amount) <= float(user.balance):
            
            serializer = BillSerializer(data=request.data)
            if serializer.is_valid():
             serializer.save(sender=user,receiver=bill_receiver)
             user.balance -= float(amount)
             user.save()
             bill_receiver.earnings += float(amount)
             bill_receiver.save()
             return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
             return Response(serializer.errors)
         
        return Response({'error': 'Insufficient funds for the bill payment.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
class PaidSearch(generics.ListAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HistoryPagination

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = Bill.objects.filter(sender=self.request.user).order_by('-timestamp')
        
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        
        return queryset
