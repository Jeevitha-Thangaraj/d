from rest_framework import serializers
from .models import ShippingAddress, ShippingRate

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '_all_'
        extra_kwargs = {'user': {'read_only': True}}

class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = '_all_'