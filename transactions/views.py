# def CashSearch(request):
#     Cash_Transaction = CashTransaction.objects.order_by('-timestamp').filter(user = request.user)
    
#     if 'start_date' in request.GET and 'end_date' in request.GET:
#      start_date = request.GET['start_date']
#      end_date = request.GET['end_date']
#      if start_date and end_date:
#          Cash_Transaction = Cash_Transaction.filter(timestamp__range=[start_date, end_date])

#     context = {
#         'Cash_History': Cash_Transaction,
#     }
#     return render(request, 'transactions/CashSearch.html', context)

# def SentSearch(request):
#     Sent_History = UserTransaction.objects.order_by('-timestamp').filter(sender = request.user)
    
#     if 'start_date' in request.GET and 'end_date' in request.GET:
#      start_date = request.GET['start_date']
#      end_date = request.GET['end_date']
#      if start_date and end_date:
#          Sent_History = Sent_History.filter(timestamp__range=[start_date, end_date])

#     context = {
#         'Sent_History': Sent_History,
#     }
#     return render(request, 'transactions/SentSearch.html', context)

# def ReceivedSearch(request):
#     Received_History = UserTransaction.objects.order_by('-timestamp').filter(receiver = request.user)
    
#     if 'start_date' in request.GET and 'end_date' in request.GET:
#      start_date = request.GET['start_date']
#      end_date = request.GET['end_date']
#      if start_date and end_date:
#          Received_History = Received_History.filter(timestamp__range=[start_date, end_date])

#     context = {
#         'Received_History': Received_History,
#     }
#     return render(request, 'transactions/ReceivedSearch.html', context)



           

