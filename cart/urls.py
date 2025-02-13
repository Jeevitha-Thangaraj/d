from django.urls import path
from .views import get_cart, add_to_cart, update_cart, remove_from_cart, clear_cart

urlpatterns = [
    path('cart/', get_cart),
    path('cart/add/', add_to_cart),
    path('cart/update/<int:cart_id>/', update_cart),
    path('cart/remove/<int:cart_id>/', remove_from_cart),
    path('cart/clear/', clear_cart),
]