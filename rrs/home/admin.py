from django.contrib import admin
from .models import *

# Register your models here.
class UserMasterAdmin(admin.ModelAdmin):
    list_display = ('username','password')
    search_fields = ['username']

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Admin Panel"    
admin.site.register(user_master)
admin.site.register(station_master)
admin.site.register(user_feedback)
admin.site.register(train_master)
admin.site.register(train_schedule)
# admin.site.register(passenger_master)
admin.site.register(class_master)
admin.site.register(RouteMaster)
admin.site.register(ScheduleMaster)
admin.site.register(coach)
admin.site.register(seat)
admin.site.register(ticket_master)
admin.site.register(passenger_master)
admin.site.register(payment_master)



