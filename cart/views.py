from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer
from store.models import Product

# GET - Get user's cart
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# POST - Add item to cart
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product')
    quantity = request.data.get('quantity', 1)

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += int(quantity)
    else:
        cart_item.quantity = int(quantity)

    cart_item.save()
    return Response(CartSerializer(cart_item).data, status=status.HTTP_201_CREATED)

# PUT - Update cart item quantity
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity = request.data.get('quantity', cart_item.quantity)
    cart_item.save()
    return Response(CartSerializer(cart_item).data, status=status.HTTP_200_OK)

# DELETE - Remove item from cart
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

# DELETE - Clear entire cart
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)
