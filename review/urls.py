from django.urls import path
from .views import get_reviews, add_review, update_review, delete_review

urlpatterns = [
    path('products/<int:product_id>/reviews/', get_reviews),
    path('products/<int:product_id>/reviews/add/', add_review),
    path('reviews/<int:review_id>/update/', update_review),
    path('reviews/<int:review_id>/delete/', delete_review),
]