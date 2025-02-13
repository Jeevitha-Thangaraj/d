from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from store.models import Product

# GET - Get all reviews for a product
@api_view(['GET'])
def get_reviews(request, product_id):
    try:
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

# POST - Add a review for a product
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = request.data
        review = Review.objects.create(
            user=request.user,
            product=product,
            rating=data.get('rating'),
            comment=data.get('comment')
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

# PUT - Update a review
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
        data = request.data
        review.rating = data.get('rating', review.rating)
        review.comment = data.get('comment', review.comment)
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

# DELETE - Delete a review
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
