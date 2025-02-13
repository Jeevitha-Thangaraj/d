from django.urls import path
from authentication.views import (register_user,login_user,logout_view,refresh_token,get_user,create_profile,
                                 get_admin_dashboard, get_all_users, get_all_orders,
                                 get_sales_report, get_inventory_report)



urlpatterns = [
    path('signup/', register_user),
    path('login/', login_user),
    path('logout/', logout_view),
    path('refresh/',refresh_token),
    path('get-user/<int:id>/',get_user),
    path('profile/',create_profile),
    path('admin/dashboard/', get_admin_dashboard),
    path('admin/users/', get_all_users),
    path('admin/orders/', get_all_orders),
    path('admin/reports/sales/', get_sales_report),
    path('admin/reports/inventory/', get_inventory_report)
    
]