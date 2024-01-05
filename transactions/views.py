from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from accounts.models import User
from transactions.models import CashTransaction, UserTransaction


def SendMoney(request):
    if request.method == 'POST':
        # Get form values
        recipient_Username = request.POST['recipient_Username']
        recipient_phone = request.POST['recipient_phone']
        amount = request.POST['amount']

        if not User.objects.filter(username=recipient_Username).exists():
            messages.error(request, 'This User Does Not Exist')
            return redirect('SendMoney')

        if request.user.username == recipient_Username:
            messages.error(request, 'Cannot transfer to self')
            return redirect('SendMoney')

        receiver = User.objects.get(username=recipient_Username)

        if not User.objects.filter(phonenum=recipient_phone).exists():
            messages.error(request, 'This Phone Number Does Not Exist')
            return redirect('SendMoney')

        if recipient_phone != receiver.phonenum:
            messages.error(request, 'Phone number does not match the recipient')
            return redirect('SendMoney')
        
        if int(amount)<=0:
            messages.error(request, 'Amount Must Be Valid')
            return redirect('SendMoney')

        if float(amount) <= float(getattr(request.user, 'balance')):
            User_Transaction = UserTransaction()
            User_Transaction.amount = amount
            User_Transaction.sender = request.user
            User_Transaction.receiver = receiver
            User_Transaction.save()
            request.user.balance = request.user.balance - float(amount)
            request.user.save()
            receiver.balance = receiver.balance + float(amount)
            receiver.save()
            messages.success(request, 'Amount Transfered Successfully')
        else: 
            messages.error(request, 'Insufficient Funds')

        return redirect('SendMoney')
    else: 
        return render(request,'transactions/SendMoney.html')

def CashTransactions(request):
    
    if request.method == 'POST':
        # Get form values
        amount = request.POST['amount']
        type = request.POST['transaction_type']
        
        if int(amount)<=0:
            messages.error(request, 'Amount Must Be Valid')
            return redirect('CashTransactions')
        
        if type == "Deposit":
            cash_transaction = CashTransaction()
            cash_transaction.amount = amount
            cash_transaction.type = type
            cash_transaction.user = request.user
            cash_transaction.save()
            request.user.balance = request.user.balance + float(amount)
            request.user.save()
            messages.success(request, 'Amount Deposited Successfuly')
            return redirect('CashTransactions')
        
        if type == "Withdraw" and float(amount) <= float(getattr(request.user, 'balance')):
            cash_transaction = CashTransaction()
            cash_transaction.amount = amount
            cash_transaction.type = type
            cash_transaction.user = request.user
            cash_transaction.save()
            request.user.balance = request.user.balance - float(amount)
            request.user.save()
            messages.success(request, 'Amount Withdrawed Successfuly')
            return redirect('CashTransactions')
        
        else:
            messages.error(request, 'Insufficient Funds')
            return redirect('CashTransactions')    
    else:
        return render(request, 'transactions/CashTransactions.html')
    
def CashSearch(request):
    Cash_Transaction = CashTransaction.objects.order_by('-timestamp').filter(user = request.user)
    
    if 'start_date' in request.GET and 'end_date' in request.GET:
     start_date = request.GET['start_date']
     end_date = request.GET['end_date']
     if start_date and end_date:
         Cash_Transaction = Cash_Transaction.filter(timestamp__range=[start_date, end_date])

    context = {
        'Cash_History': Cash_Transaction,
    }
    return render(request, 'transactions/CashSearch.html', context)

def SentSearch(request):
    Sent_History = UserTransaction.objects.order_by('-timestamp').filter(sender = request.user)
    
    if 'start_date' in request.GET and 'end_date' in request.GET:
     start_date = request.GET['start_date']
     end_date = request.GET['end_date']
     if start_date and end_date:
         Sent_History = Sent_History.filter(timestamp__range=[start_date, end_date])

    context = {
        'Sent_History': Sent_History,
    }
    return render(request, 'transactions/SentSearch.html', context)

def ReceivedSearch(request):
    Received_History = UserTransaction.objects.order_by('-timestamp').filter(receiver = request.user)
    
    if 'start_date' in request.GET and 'end_date' in request.GET:
     start_date = request.GET['start_date']
     end_date = request.GET['end_date']
     if start_date and end_date:
         Received_History = Received_History.filter(timestamp__range=[start_date, end_date])

    context = {
        'Received_History': Received_History,
    }
    return render(request, 'transactions/ReceivedSearch.html', context)



           

