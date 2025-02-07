from django.urls import path
from authentication.views import register_user,login_user,logout_view,refresh_token,get_user,create_profile


urlpatterns = [
    path('signup/', register_user),
    path('login/', login_user),
    path('logout/', logout_view),
    path('refresh/',refresh_token),
    path('get-user/<int:id>/',get_user),
    path('profile/',create_profile)
    
]