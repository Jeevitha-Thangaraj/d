from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from store.models import  Product
from order.models import Order,OrderItem,Payment,Cart
from .serializers import OrderSerializer,OrderIemSerializer,PaymentSerializer,CartSerializer
from django.conf import settings
import stripe


stripe.api_key=settings.STRIPE_SECRET_KEY



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return Response({"message": "Your cart is empty!"}, status=400)

    total_amount = sum(item.product.price * item.quatity for item in cart_items)

    order = Order.objects.create(user=user, total_amount=total_amount, status="pending")

    # Move items from Cart to OrderItems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
        # Reduce stock from the product
        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart after placing order
    cart_items.delete()

    return Response({"message": "Order placed successfully!", "order_id": order.id}, status=201)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response({"orders": serializer.data}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    serializer = OrderSerializer(order)
    return Response({"order": serializer.data}, status=200)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.data.get("status")

    if new_status not in ["pending", "paid", "shipped", "delivered", "cancelled"]:
        return Response({"message": "Invalid status update!"}, status=400)

    order.status = new_status
    order.save()
    return Response({"message": f"Order status updated to {new_status}!"}, status=200)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != "pending":
        return Response({"message": "You can only cancel pending orders."}, status=400)

    order.status = "cancelled"



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def make_payment(request):
    order_id = request.data.get("order_id")
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"message": "Order not found"}, status=404)

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),  # Convert to cents
            currency="usd",
            payment_method=request.data.get("token"),
            confirmation_method="manual",
            confirm=True,
        )
        order.status = 'paid'
        order.save()
        return Response({"message": "Payment successful", "payment_intent": payment_intent.id}, status=200)
    except stripe.error.CardError as e:
        return Response({"message": str(e)}, status=400)
