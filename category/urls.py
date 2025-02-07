from django.urls import path
from .views import get_categories, get_category, create_category, update_category, delete_category

urlpatterns = [
    path('categories/', get_categories),
    path('categories/<int:category_id>/', get_category),
    path('categories/create/', create_category),
    path('categories/update/<int:category_id>/', update_category),
    path('categories/delete/<int:category_id>/', delete_category),
]