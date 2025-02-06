from django.urls import path
from .views import create_product, update_product, search_products

urlpatterns = [
    path("products/create/", create_product),
    path("products/update/<int:id>/", update_product),
    path("products/search/", search_products),
]