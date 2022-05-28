from django.urls import path
from . import views



app_name = "orders"

# URLConf
urlpatterns =   [
    path('place_order/', views.place_order,name='place_order') ,
    path('confirm_order/', views.confirm_order,name='confirm_order') ,
    path('order_complete/', views.order_complete,name='order_complete') ,
                ]

