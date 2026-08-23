from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from products.serializers import ProductSerializer,CategorySerializer
from rest_framework.permissions import AllowAny
from products.models import Product,Category
from django.shortcuts import get_object_or_404
# Create your views here.

class ProductView(ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=ProductSerializer
    def get_queryset(self):
        queryset=Product.objects.all()
        category=self.request.query_params.get('category')
        ordering=self.request.query_params.get('ordering')
        if category:
            queryset=queryset.filter(category__category_slug=category)
        if ordering in ['price','-price']:
            queryset=queryset.order_by(ordering)
        return queryset

class CategoryView(ListAPIView):
    queryset=Category.objects.all()
    permission_classes=[AllowAny]
    serializer_class=CategorySerializer

class ProductDetailView(RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]
    lookup_field='product_slug'

class RelatedProductsView(ListAPIView):

    serializer_class=ProductSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        product=get_object_or_404(Product,product_slug=self.kwargs['product_slug'])
        return Product.objects.filter(category=product.category).exclude(pk=product.pk)
    