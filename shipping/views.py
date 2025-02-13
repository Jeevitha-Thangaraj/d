from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ShippingAddress, ShippingRate
from .serializers import ShippingAddressSerializer, ShippingRateSerializer

# GET - Get available shipping rates
@api_view(['GET'])
def get_shipping_rates(request):
    rates = ShippingRate.objects.all()
    serializer = ShippingRateSerializer(rates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# GET - Track shipping status (Dummy response for now)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_shipping(request, tracking_id):
    dummy_tracking_status = {
        "tracking_id": tracking_id,
        "status": "In Transit",
        "expected_delivery": "2025-02-10"
    }
    return Response(dummy_tracking_status, status=status.HTTP_200_OK)

# GET - Get user shipping address
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shipping_address(request):
    try:
        address = ShippingAddress.objects.get(user=request.user)
        serializer = ShippingAddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ShippingAddress.DoesNotExist:
        return Response({"error": "Shipping address not found"}, status=status.HTTP_404_NOT_FOUND)

# POST - Add or update shipping address
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_update_shipping_address(request):
    try:
        address = ShippingAddress.objects.get(user=request.user)
        serializer = ShippingAddressSerializer(address, data=request.data, partial=True)
    except ShippingAddress.DoesNotExist:
        serializer = ShippingAddressSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
