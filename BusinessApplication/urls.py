"""
URL configuration for BusinessApplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from functions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('showBOM/', views.showBOM, name='showBOM'),
    path('addBOM', views.addBOM, name='addBOM'),
    path('showInventory', views.showInventory, name='showInventory'),
    path('addInventory', views.addInventory, name='addInventory'),
    path('showSupplier', views.showSupplier, name='showSupplier'),
    path('addSupplier', views.addSupplier, name='addSupplier'),
    path('showCustomer', views.showCustomer, name='showCustomer'),
    path('addCustomer', views.addCustomer, name='addCustomer'),
    path('showOrder', views.showOrder, name='showOrder'),
    path('addOrder', views.addOrder, name='addOrder'),
    path('showWalkIn', views.showWalkIn, name='showWalkIn'),
    path('addWalkIn', views.addWalkIn, name='addWalkIn'),
    path('analysis', views.analysis, name='analysis'),
]
