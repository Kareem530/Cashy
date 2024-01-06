from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
 list_display = ('id','username','first_name','last_name','email','is_staff','is_active','phonenum')
 list_display_links = ('id', 'username')
 list_editable = ('is_active',)
 search_fields = ('username',)
 User_per_page = 25


admin.site.register(User,UserAdmin)