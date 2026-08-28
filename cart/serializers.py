from rest_framework import serializers
from cart.models import CartItem
    
class CartItemCreateSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="product.name",read_only=True)
    
    class Meta:
        model=CartItem
        fields=['id','product','product_name','quantity','sub_total']
        read_only_fields=['id','product_name','sub_total']

class CartItemUpdateSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="product.name",read_only=True)
    
    class Meta:
        model=CartItem
        fields=['id','product','product_name','quantity','sub_total']
        read_only_fields=['product','sub_total']