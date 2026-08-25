from django.contrib import admin
from orders.models import OrderItem, Order, TrackingDetail
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','status','total_amount','created_at','updated_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','unit_price']

@admin.register(TrackingDetail)
class TrackingDetailAdmin(admin.ModelAdmin):
    list_display=['id','order','status','location','notes','updated_at']