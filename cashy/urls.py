from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path("", include('pages.urls')),
    path("accounts/", include('accounts.urls')),
    path("transactions/", include('transactions.urls')),
    path("bills/", include('bills.urls')),
    path("", include('contact.urls')),
    path("admin/", admin.site.urls),
]
