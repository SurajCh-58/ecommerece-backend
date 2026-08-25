from rest_framework import serializers
from orders.models import Order, OrderItem, TrackingDetail

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','product','quantity','unit_price','sub_total']
        read_only_fields=['id','product','quantity','unit_price','sub_total']


class TrackingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrackingDetail
        fields=['id','status','location','notes','updated_at']
        read_only_fields=['id','status','location','notes','updated_at']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    tracking_details=TrackingDetailSerializer(many=True,read_only=True)
    class Meta:
        model=Order

        fields=['id','status','total_amount','created_at','updated_at','items','tracking_details']
        read_only_fields=['id','status','total_amount','created_at','updated_at','tracking_details']