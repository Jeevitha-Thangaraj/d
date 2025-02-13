from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ['user']