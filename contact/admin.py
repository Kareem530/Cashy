from django.contrib import admin

from .models import Contact
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
 list_display = ('id','name','email','subject','message','date','user')
 list_display_links = ('name', 'id')
 search_fields = ('subject',)
 Contact_per_page = 25


admin.site.register(Contact,ContactAdmin)