from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('accounts.api.urls')),
    path("bills/", include('bills.api.urls')),
    path("transactions/", include('transactions.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),    
]
