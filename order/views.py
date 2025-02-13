from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from store.models import Product

# GET - Get user's order history
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_history(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# GET - Get order details by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_details(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

# POST - Create a new order
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    items = request.data.get('items', [])
    
    if not items:
        return Response({"error": "Order must contain at least one item"}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(user=request.user, total_price=0)
    total_price = 0

    for item in items:
        try:
            product = Product.objects.get(id=item['product_id'])
            quantity = int(item['quantity'])
            price = product.price * quantity

            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            total_price += price
        except Product.DoesNotExist:
            return Response({"error": f"Product with ID {item['product_id']} not found"}, status=status.HTTP_404_NOT_FOUND)

    order.total_price = total_price
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# PUT - Cancel an order
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.status in ['shipped', 'delivered']:
            return Response({"error": "Cannot cancel an order that is already shipped or delivered"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()
        return Response({"message": "Order cancelled successfully"}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

# GET - Get order tracking details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        return Response({"order_id": order.id, "status": order.status}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)