from django.contrib import admin
from .models import BillCompany

# Register your models here.
class BillCompanyAdmin(admin.ModelAdmin):
 list_display = ('company_id','company_name','is_active','earnings')
 list_display_links = ('company_id', 'company_name')
 list_editable = ('is_active',)
 search_fields = ('company_name',)
 BillCompany_per_page = 25


admin.site.register(BillCompany,BillCompanyAdmin)