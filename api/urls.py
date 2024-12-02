from django.urls import path
from .views import get_products, create_order, get_product, get_orders, put_order

urlpatterns = [
    path('products/', get_products, name='product-list'),
    path('products/<int:id>/', get_product, name='product-detail'),
    path('create-order/', create_order, name='create_order'),
    path('orders/', get_orders, name="get_orders"),
    path('orders/<int:id>/complete/', put_order, name='complete_order'),
]
