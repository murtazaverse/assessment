from django.urls import path
from .views import *

urlpatterns = [

    path('create_orders/', CreateOrders.as_view(), name="create_orders"),
    path('fetch_update_delete_orders/', ReadUpdateDeleteOrders.as_view(), name="order_RUD"),
    path('create_user/', CreateUser.as_view(), name="create_user"),
    path('fetch_update_delete_users/', ReadUpdateDeleteUsers.as_view(), name="user_RUD"),
    path('user_emails/', UserEmailList.as_view(), name="user_emails"),
    path('user_orders/', OrderByUserEmail.as_view(), name="user_orders"),
    path('login/', Login.as_view(), name='login'),
    
]