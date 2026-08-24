from rest_framework import serializers
from products.models import Category,Product

class ProductSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    class Meta:
        model=Product
        fields=['id','image','name','description','price','category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name']        