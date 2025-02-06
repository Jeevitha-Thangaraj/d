from django.urls import path
from authentication.views import signup_user,login_user,logout_view


urlpatterns = [
    path('signup/', signup_user),
    path('login/', login_user),
    path('logout/', logout_view),
    
]