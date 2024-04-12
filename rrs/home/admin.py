from django.contrib import admin
from .models import user_master

# Register your models here.
class UserMasterAdmin(admin.ModelAdmin):
    list_display = ('username','password')
    search_fields = ['username']
    
admin.site.register(user_master,UserMasterAdmin)

