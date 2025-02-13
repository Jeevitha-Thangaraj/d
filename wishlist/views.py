from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Wishlist
from wishlist.serializers import WishlistSerializer
from store.models import Product  

# GET - Get user's wishlist
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    serializer = WishlistSerializer(wishlist_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# POST - Add product to wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            return Response({"message": "Product added to wishlist"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Product already in wishlist"}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

# DELETE - Remove product from wishlist
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request):
    product_id = request.data.get('product_id')
    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    wishlist_item = Wishlist.objects.filter(user=request.user, product_id=product_id).first()
    if wishlist_item:
        wishlist_item.delete()
        return Response({"message": "Product removed from wishlist"}, status=status.HTTP_200_OK)
    
    return Response({"error": "Product not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)
