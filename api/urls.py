from django.urls import path
from .views import get_products, create_order

urlpatterns = [
    path('products/', get_products, name='product-list'),
    path('create-order/', create_order, name='create_order'),
]
