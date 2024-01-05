from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import User
from .models import BillCompany, Bill


def Paybills(request):
    bill_companies = BillCompany.objects.filter(is_active=True)
    context = {
        'bill_companies': bill_companies,
    }
    
    if request.method == 'POST':
        
        bill_company = request.POST['bill_company']
        amount = request.POST['amount']
        
        if int(amount)<=0:
            messages.error(request, 'Amount Must Be Valid')
            return redirect('Paybills')
        
        if float(amount) < float(getattr(request.user, 'balance')):
                
                Bill_Transaction = Bill()
                Bill_Transaction.amount = amount
                Bill_Transaction.sender = request.user
                receiver = BillCompany.objects.get(company_name=bill_company)
                Bill_Transaction.receiver = receiver
                Bill_Transaction.save()
                request.user.balance = request.user.balance - float(amount)
                request.user.save()
                receiver.earnings = receiver.earnings + float(amount)
                receiver.save()
                messages.success(request, 'Amount Transfered Successfuly')
                return redirect('Paybills')
            
        else: 
            messages.error(request, 'Insufficient Funds')
            return redirect('Paybills')
        
    else:
        return render(request, 'bills/Paybills.html', context)

def PaidSearch(request):
    Paid_History = Bill.objects.order_by('-timestamp').filter(sender = request.user)
    
    if 'start_date' in request.GET and 'end_date' in request.GET:
     start_date = request.GET['start_date']
     end_date = request.GET['end_date']
     if start_date and end_date:
         Paid_History = Paid_History.filter(timestamp__range=[start_date, end_date])

    context = {
        'Paid_History': Paid_History,
    }
    return render(request, 'bills/PaidSearch.html', context)