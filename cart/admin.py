from django.contrib import admin
from cart.models import Cart,CartItem
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','created_at','updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','cart','product','quantity','added_at']