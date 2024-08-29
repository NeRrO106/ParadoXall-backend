from django.contrib import admin
from .models import Order, Order_Item, Product

admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(Product)