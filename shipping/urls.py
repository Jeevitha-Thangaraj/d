from django.urls import path
from .views import get_shipping_rates, track_shipping, get_shipping_address, add_update_shipping_address

urlpatterns = [
    path('shipping/rates/', get_shipping_rates),
    path('shipping/track/<str:tracking_id>/', track_shipping),
    path('shipping/address/', get_shipping_address),
    path('shipping/address/update/', add_update_shipping_address),
]