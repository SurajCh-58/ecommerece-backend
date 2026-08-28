from rest_framework import serializers
from payment.serializers import PaymentSerializer
from orders.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price','sub_total']
        read_only_fields=['id','product','quantity','unit_price','sub_total']


class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    payment=PaymentSerializer(read_only=True)
    class Meta:
        model=Order

        fields=['id',
                'status',
                'total_amount',
                'shipping_name',
                'shipping_phone',
                'shipping_state',
                'shipping_city',
                'shipping_address',
                'shipping_postal_code',
                'created_at',
                'updated_at',
                'items',
                'payment']
        read_only_fields=['id',
                          'status',
                          'total_amount',
                          'created_at',
                          'updated_at',
                          'payment']