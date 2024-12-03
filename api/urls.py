from django.urls import path
from .views import get_products, create_order, get_product, get_orders, put_order, delete_product, edit_product, create_product

urlpatterns = [
    path('products/', get_products, name='product-list'),
    path('products/<int:id>/', get_product, name='product-detail'),
    path('create-order/', create_order, name='create_order'),
    path('add-product', create_product, name='create_product'),
    path('orders/', get_orders, name="get_orders"),
    path('orders/<int:id>/complete/', put_order, name='complete_order'),
    path('delete-product/<int:id>/', delete_product, name="delete_product"),
    path('edit-product/<int:id>/', edit_product, name="edit_product"),
]
