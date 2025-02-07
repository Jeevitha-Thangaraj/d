from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Product
from store.serializers import ProductSerializer
from rest_framework import status

@api_view(["POST"])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Product created successfully", "data": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_products(request):
    products=Product.objects.all()
    serializers=ProductSerializer(products,many=True)
    return Response({"data":serializers.data},status=status.HTTP_200_OK)


@api_view(["GET"])
def get_product(request,product_id):
    try:
        product=Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_product(request, id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product updated successfully", "data": serializer.data}, status=200)
    except Product.DoesNotExist:
        return Response({"message": "Product not found"}, status=404)

@api_view(["GET"])
def search_products(request):
    query = request.get("q", "")
    category = request.get("category", "")

    products = Product.objects.all()
    if query:
        products = products.filter(Q(name_icontains=query) | Q(description_icontains=query))
    if category:
        products = products.filter(category__iexact=category)

    serializer = ProductSerializer(products, many=True)
    return Response({"data": serializer.data}, status=200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({'message': 'Product delete successfully'},status=status.HTTP_204_NO_CONTENT)