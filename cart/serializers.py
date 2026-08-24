from rest_framework import serializers
from cart.models import Cart,CartItem

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','user']
        read_only_fields=['user']
    
class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['product','quantity',]

class CartItemReadSerializer(serializers.ModelSerializer):
    cart=serializers.StringRelatedField()
    product=serializers.StringRelatedField()
    class Meta:
        model=CartItem
        fields=['id','cart','product','quantity',]