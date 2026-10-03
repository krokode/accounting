from django.urls import path
from apps.warehouse import views

app_name = 'warehouse'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('consignments/', views.consignment_list, name='consignment_list'),
    path('consignments/<int:pk>/', views.consignment_detail, name='consignment_detail'),
    path('consignments/<int:pk>/confirm/', views.consignment_confirm, name='consignment_confirm'),
]
