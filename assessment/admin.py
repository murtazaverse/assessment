from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('order_details', 'order_total','user')

admin.site.register(Order, OrderAdmin)