from django.db import models
from orders.models import Order

# Create your models here.
class Payment(models.Model):
    class Method(models.TextChoices):
        COD='cod','Cash on Delivery'
        ESEWA='esewa','Esewa'
        KHALTI='khalti','Khalti'
        CARD='card','CARD'
    class Status(models.TextChoices):
        PENDING='pending','Pending'
        PAID='paid','Paid'
        FAILED='failed','Failed'
        REFUNDED='refunded','Refunded'
    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name='payment')
    method=models.CharField(max_length=20,choices=Method.choices)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    status=models.CharField(max_length=20,choices=Status.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    
