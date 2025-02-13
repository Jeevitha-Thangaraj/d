from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = Review
        fields ="__all__"