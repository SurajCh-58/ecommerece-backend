from django.contrib import admin
from orders.models import OrderItem, Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','status','total_amount','shipping_name','shipping_phone','shipping_state','shipping_city','shipping_address','shipping_postal_code','created_at','updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','unit_price']