from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.

class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Cart #{self.id} for {self.user}"
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    quantity=models.PositiveIntegerField(default=1)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def sub_total(self):
        return self.product.price*self.quantity