from rest_framework import serializers
from payment.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order=serializers.StringRelatedField()
    class Meta:
        model=Payment

        fields=['id','order','method','amount','status']

        read_only_fields=['id','order','method','amount','status']

class CheckoutSerializer(serializers.Serializer):
    address_id=serializers.IntegerField()
    payment_method=serializers.ChoiceField(choices=Payment.Method.choices)