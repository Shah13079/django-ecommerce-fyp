"""Crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings
from Crawler.settings import MEDIA_ROOT

admin.site.site_header = "Shah Cart"


urlpatterns = [ path('admin-hussain/', admin.site.urls),
                #apps
               
                path('', include('my_store.urls')),
                path('cart/', include('cart.urls')),
                path('orders/', include('orders.urls')),
       
                path('accounts/',include('accounts.urls')),
           
                
                
                ]+ static(settings.MEDIA_URL,document_root=MEDIA_ROOT)
                

                


