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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('showBOM', views.showBOM, name='showBOM'),
    path('addBOM', views.addBOM, name='addBOM'),
    path('showMaterial', views.showMaterial, name='showMaterial'),
    path('addMaterial', views.addMaterial, name='addMaterial'),
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
    #表單提交
    path('submitSupplier', views.submitSupplier, name='submitSupplier'),
    path('updateSupplier', views.updateSupplier, name='updateSupplier'),
    path('submitMaterial', views.submitMaterial, name='submitMaterial'),
    path('updateMaterial', views.updateMaterial, name='updateMaterial'),
    path('submitBOM', views.submitBOM, name='submitBOM'),
    path('updateBOM', views.updateBOM, name='updateBOM'),
    path('submitCustomer', views.submitCustomer, name='submitCustomer'),
    path('updateCustomer', views.updateCustomer, name='updateCustomer'),
    path('submitOrder', views.submitOrder, name='submitOrder'),

    #生成表格
    path('getSupplierList', views.getSupplierList, name='getSupplierList'),
    path('getMaterialList', views.getMaterialList, name='getMaterialList'),
    path('getBOMList', views.getBOMList, name='getBOMList'),
    path('getCustomerList', views.getCustomerList, name='getCustomerList'),
    path('getOneTimeOrderList', views.getOneTimeOrderList, name='getOneTimeOrderList'),
    path('getRecurringOrderList', views.getRecurringOrderList, name='getRecurringOrderList'),

    #刪除資料
    path('deleteSupplier', views.deleteSupplier, name='deleteSupplier'),
    path('deleteMaterial', views.deleteMaterial, name='deleteMaterial'),
    path('deleteProduct', views.deleteProduct, name='deleteProduct'),
    path('deleteCustomer', views.deleteCustomer, name='deleteCustomer'),
    path('deleteOrder', views.deleteOrder, name='deleteOrder'),
    #修改資料
    path('editProduct/<int:productID>/', views.editProduct, name='editProduct'),
    path('editOrder/<int:orderID>/', views.editOrder, name='editOrder'),
]
