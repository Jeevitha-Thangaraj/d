from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from category.serializer import CategorySerializer

# Get all product categories
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.filter(parent_category__isnull=True)  # Top-level categories
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# Get specific category details
@api_view(['GET'])
def get_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category)
    return Response(serializer.data)

# Create a new category (Admin only)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update category details (Admin only)
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete a category (Admin only)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    category.delete()
    return Response({"message":"category deleted successfully"},status=status.HTTP_204_NO_CONTENT)