from django.urls import path
from order.views import  place_order,user_orders, order_detail,update_order_status,cancel_order,make_payment

urlpatterns = [
    path("products/order/",place_order),
    path('orders/',user_orders),
    path("order-details/<int:order_id>/",order_detail),
    path("update/<int:order_id>/",update_order_status),
    path("cancel/<int:order_id>/",cancel_order),
    path("payments/", make_payment),
]