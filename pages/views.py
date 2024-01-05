from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'pages/Home.html')

def about(request):
    return render(request,'pages/About.html')

def services(request):
    return render(request,'pages/Services.html')
