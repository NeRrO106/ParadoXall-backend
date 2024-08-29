from rest_framework import serializers
from .models import Order, Order_Item

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Item
        fields = ['product', 'quantity', 'selected_option']

class OrderSerializer(serializers.ModelSerializer):
    
    order_items = OrderItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Order
        fields= [
            'customer_name', 'phone_number', 'email', 
            'delivery_method', 'address', 'city', 'region', 
            'payment_methods', 'additional_info', 'order_items',
            'total_amount'
        ]

    def create(self, validate_data):
        order_items_data = validate_data.pop('order_items')

        order = Order.objects.create(**validate_data)

        for item_data in order_items_data:
            Order_Item.objects.create(order=order, **item_data)
        return order 