from django.urls import path
from .views import get_wishlist, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('wishlist/', get_wishlist),
    path('wishlist/add/', add_to_wishlist),
    path('wishlist/remove/', remove_from_wishlist),
]