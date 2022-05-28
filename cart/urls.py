from django.urls import path
from . import views

app_name = "cart"

# URLConf
urlpatterns = [
    path('add_cart/<int:product_id>/', views.add_cart,name='add_cart'),
    path('mycart/', views.cart,name='mycart'),
    path('checkout/', views.checkout,name='checkout'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.decrement_item,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item,name='remove_cart_item'),
    

            ]