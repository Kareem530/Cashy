from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.models import User
from bills.models import Bill
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from transactions.models import CashTransaction, UserTransaction

import re

def register(request): #If POST, then register user and redirect, otherwise render template
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        phonenum = request.POST['phonenum']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phonenum_pattern = r'^01[0-2][0-9]{8}$'

        if not re.match(email_pattern, email):
         messages.error(request, 'Please enter a valid email address')
         return redirect('Register')
     
        # Check if passwords match
        if password == password2:
            # Check for new username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('Register')
            
            if not re.match(phonenum_pattern, phonenum):
                messages.error(request, 'Please enter a valid Egyptian phone number')
                return redirect('Register')
            
            if User.objects.filter(phonenum=phonenum).exists():
                messages.error(request, 'That Phone number is being used')
                return redirect('Register')
            
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('Register')
                else:
                    # Looks good
                    user = User.objects.create_user(
                        username=username, 
                        password=password,
                        phonenum = phonenum, 
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('Login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('Register')
    else:
        return render(request, 'accounts/Register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('Dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('Login')
    else:
        return render(request, 'accounts/Login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('Home')

def dashboard(request):
    
    Cash_Transactions = CashTransaction.objects.filter(user = request.user)
    Sent_Transactions = UserTransaction.objects.filter(sender = request.user) 
    Received_Transactions = UserTransaction.objects.filter(receiver = request.user)
    Paid_Bills = Bill.objects.filter(sender = request.user)
    
    context = {
        'Cash_Transactions': Cash_Transactions.order_by('-timestamp')[:10],
        'Sent_Transactions': Sent_Transactions.order_by('-timestamp')[:10],
        'Received_Transactions': Received_Transactions.order_by('-timestamp')[:10],
        'Paid_Bills': Paid_Bills.order_by('-timestamp')[:10],
    }
    
    return render(request, 'accounts/Dashboard.html', context)

def Cash_History(request):

    Cash_History = CashTransaction.objects.order_by('-timestamp').filter(user = request.user)   
    Cash_paginator = Paginator(Cash_History, 1)
    page = request.GET.get('page')
    paged_Cash = Cash_paginator.get_page(page)

    context = {
        'Cash_History': paged_Cash,
    }
    
    return render(request, 'accounts/Cash_History.html', context)

def Sent_History (request):

    Sent_History = UserTransaction.objects.order_by('-timestamp').filter(sender = request.user)
    Sent_paginator = Paginator(Sent_History, 1)
    page = request.GET.get('page')
    paged_Sent = Sent_paginator.get_page(page)

    context = {
        'Sent_History': paged_Sent,
    }
    
    return render(request, 'accounts/Sent_History.html', context)

def Received_History (request):

    Received_History = UserTransaction.objects.order_by('-timestamp').filter(receiver = request.user)
    Received_paginator = Paginator(Received_History,1)
    page = request.GET.get('page')
    paged_Received = Received_paginator.get_page(page)

    context = {
        'Received_History': paged_Received,
    }
    
    return render(request, 'accounts/Received_History.html', context)

def Paid_History (request):

    Paid_History = Bill.objects.order_by('-timestamp').filter(sender = request.user)
    Paid_paginator = Paginator(Paid_History,1)
    page = request.GET.get('page')
    paged_Paid = Paid_paginator.get_page(page)

    context = {
        'Paid_History': paged_Paid,
    }
    
    return render(request, 'accounts/Paid_History.html', context)