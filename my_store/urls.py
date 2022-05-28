from argparse import Namespace
from django.urls import path
from . import views

app_name = "my_store"

urlpatterns = [
    path('', views.home_producs,name='store'),
    path('products/', views.store_products,name='products'),
    path('search/', views.search,name='search'),
    path('category/<slug:category_slug>/', views.store_products,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail,name='product_detail')
    
   
            ]
