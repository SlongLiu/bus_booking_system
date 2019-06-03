"""bus_booking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
# from django.urls import path
from django.urls import path,re_path
from django.conf.urls import url
from booking import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('firstpage/', views.first_request),
    path('index/', views.index, name='index'),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('base/', views.base),
    # path('captcha/', include('captcha.urls')),
    url(r'^captcha', include('captcha.urls')),
    path('browse/', views.browse),
    path('booking/', views.booking, name='booking'),
    path('np-result/', views.no_result),
    path('result/', views.result, name='result'),
    path('', views.index),
    path('validation/', views.validation, name='validation'),
    path('manage/', views.manage),
    path('management/', views.manage),
    path('manage_orders/', views.manage_orders),
    re_path(r'manage_orders/(\d+)/del/$', views.del_order)
]
