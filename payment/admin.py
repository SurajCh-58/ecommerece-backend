from django.contrib import admin
from payment.models import Payment
# Register your models here.

@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display=['id','order','method','amount','status','created_at']