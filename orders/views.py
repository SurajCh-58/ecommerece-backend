from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from django.db import transaction
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from payment.serializers import CheckoutSerializer
from payment.models import Payment
from accounts.models import Address
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from decimal import Decimal
# Create your views here.

class OrderCreateView(CreateAPIView):
    serializer_class=CheckoutSerializer
    permission_classes=[IsAuthenticated]

    @transaction.atomic
    def create(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address_id=serializer.validated_data['address_id']
        payment_method=serializer.validated_data['payment_method']

        address=Address.objects.filter(id=address_id).first()
        if not address:
            raise ValidationError("Invalid delivery address.")

        profile=request.user.profile

        cart=Cart.objects.filter(user=self.request.user).first()
        if not cart:
            raise ValidationError("Cart does not exist.")
        cart_items=cart.cart_item.all()

        if not cart_items.exists():
            raise ValidationError("Cart is empty.")

        if not profile.full_name:
            raise ValidationError({
                "full_name":"please add your fullname before checkout"}
            )
        if not profile.phone_number:
            raise ValidationError({
                "phone_number":"please add your phone number before checkout"})
        order=Order.objects.create(user=self.request.user,
                                   total_amount=Decimal('0'),
                                   shipping_name=profile.full_name,
                                   shipping_phone=profile.phone_number,
                                   shipping_state=address.state,
                                   shipping_city=address.city,
                                   shipping_address=address.address_line,
                                   shipping_postal_code=address.postal_code)
        total_amount=Decimal("0")
        for cart_item in cart_items:
            unit_price=cart_item.product.price
            OrderItem.objects.create(order=order,product=cart_item.product,quantity=cart_item.quantity,unit_price=unit_price)
            total_amount += (unit_price*cart_item.quantity)
        order.total_amount=total_amount
        order.save()
        Payment.objects.create(order=order,method=payment_method,amount=total_amount)
        cart_items.delete()

        return Response(OrderSerializer(order).data,status=status.HTTP_201_CREATED)
    
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