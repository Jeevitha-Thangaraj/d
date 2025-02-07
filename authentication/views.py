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
    