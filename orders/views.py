from django.shortcuts import render
from django.db import transaction
from orders.models import Order, OrderItem, TrackingDetail
from orders.serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart
from decimal import Decimal
# Create your views here.

class OrderCreateView(CreateAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    @transaction.atomic
    def create(self,request,*args,**kwargs):
        cart=Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'message':'cart does not  exists'},status=status.HTTP_400_BAD_REQUEST)
        cart_items=cart.cart_item.all()

        if not cart_items.exists():
            return Response({'message':'your cart is empty'},status=status.HTTP_400_BAD_REQUEST)

        order=Order.objects.create(user=request.user,total_amount=0)

        total_amount=Decimal('0')
        for cart_item in cart_items:
            unit_price=cart_item.product.price
            OrderItem.objects.create(order=order,product=cart_item.product,quantity=cart_item.quantity,unit_price=unit_price)
            total_amount+=unit_price*cart_item.quantity
        order.total_amount=total_amount
        order.save()

        TrackingDetail.objects.create(order=order,status="order placed")

        cart_items.delete()

        return Response({'message':'order has been placed sucessfully.'},status=status.HTTP_202_ACCEPTED)
    
class OrderListView(ListAPIView):

    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
       return Order.objects.filter(user=self.request.user).order_by("-created_at")

class OrderReteriveView(RetrieveAPIView):

    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
       return Order.objects.filter(user=self.request.user)       