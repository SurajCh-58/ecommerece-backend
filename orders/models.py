from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING="pending","Pending"
        CONFIRMED="confirmed","Confirmed"
        PROCESSING="processing","Processing"
        SHIPPED="shipped","Shipped"
        DELIVERED="delivered","Delivered"
        CANCELLED="cancelled","Cancelled"

    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='orders')
    status=models.CharField(max_length=12,choices=Status.choices,default=Status.PENDING)
    total_amount=models.DecimalField(max_digits=12,decimal_places=2)
    quantity=models.IntegerField()
    shipping_name=models.CharField(max_length=100)
    shipping_phone=models.CharField(max_length=20)
    shipping_state=models.CharField(max_length=100)
    shipping_city=models.CharField(max_length=100)
    shipping_address=models.CharField(max_length=100)
    shipping_postal_code=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    quantity=models.PositiveIntegerField(default=1)
    unit_price=models.DecimalField(max_digits=12,decimal_places=2)

    @property
    def sub_total(self):
        return self.unit_price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
