from django.urls import path
from .views import get_order_history, get_order_details, create_order, cancel_order, track_order

urlpatterns = [
    path('orders/', get_order_history),
    path('orders/<int:order_id>/', get_order_details),
    path('orders/create/', create_order),
    path('orders/<int:order_id>/cancel/', cancel_order),
    path('orders/<int:order_id>/track/', track_order),
]