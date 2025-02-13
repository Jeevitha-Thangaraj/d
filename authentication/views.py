from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from authentication.serializer import  UserSerializer,ProfileSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from order.models import Order
from store.models import Product
from authentication.permissions import IsAdminUserCustom




@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "User registed successfully"},status=status.HTTP_201_CREATED)

@api_view(["POST"])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
    token = AccessToken.for_user(user)
    response = Response({'message': 'Logged in successfully'},status=status.HTTP_200_OK)
    
    # Set JWT as HttpOnly cookie
    response.set_cookie(
        key='jwt',
        value=str(token),
        httponly=True,
        samesite='Strict', # Optional: To prevent CSRF
        max_age=365 * 24 * 60 * 60, # 1 year
    )
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    response = Response({'message': 'Logged out successfully'},
    status=status.HTTP_200_OK)
    # Clear the cookie
    response.delete_cookie('jwt')
    return response

@api_view(['POST'])
def refresh_token(request):
    refresh = request.data.get('refresh')
    if not refresh:
        return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh)
        return Response({'access': str(token.access_token)}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def get_user(request,id):
    try:
        user=User.objects.get(id=id)
        serializer=UserSerializer(user)
        return Response({"message":"user fetched successfully","data":serializer.data},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message":"user Does not exist"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_profile(request):
    user_id = request.user.id
    request.data["user"] = user_id
    serializer = ProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Profile created successfully", "data": serializer.data}, status=201)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(
        instance=profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message":"profile updated successfully ","data":serializer.data},status=status.HTTP_200_OK)



# GET - Get admin dashboard statistics
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def get_admin_dashboard(request):
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_sales = sum(order.total_price for order in Order.objects.all())
    total_products = Product.objects.count()

    return Response({
        "total_users": total_users,
        "total_orders": total_orders,
        "total_sales": total_sales,
        "total_products": total_products
    }, status=status.HTTP_200_OK)

# GET - Get all users (Admin)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def get_all_users(request):
    users = User.objects.values('id', 'username', 'email', 'is_staff', 'date_joined')
    return Response(users, status=status.HTTP_200_OK)

# GET - Get all orders (Admin)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def get_all_orders(request):
    orders = Order.objects.values('id', 'user__username', 'status', 'total_price', 'created_at')
    return Response(orders, status=status.HTTP_200_OK)

# GET - Get sales reports
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def get_sales_report(request):
    orders = Order.objects.all()
    total_sales = sum(order.total_price for order in orders)
    report = [{"order_id": order.id, "user": order.user.username, "total_price": order.total_price} for order in orders]

    return Response({"total_sales": total_sales, "orders": report}, status=status.HTTP_200_OK)

# GET - Get inventory report
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUserCustom])
def get_inventory_report(request):
    products = Product.objects.values('id', 'name', 'price', 'stock')
    return Response(products, status=status.HTTP_200_OK)
    