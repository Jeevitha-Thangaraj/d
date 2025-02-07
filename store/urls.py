from django.urls import path
from .views import create_product, get_product,get_products,update_product, search_products,delete_product

urlpatterns = [
    path("products/create/", create_product),
    path("get-products/",get_products),
    path("get-product/<int:product_id>/",get_product),
    path("products/update/<int:id>/", update_product),
    path("products/search/", search_products),
    path("products/delete/<int:product_id>/",delete_product),

]