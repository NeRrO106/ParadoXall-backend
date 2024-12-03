from django.http import JsonResponse
from .models import Product, Order, Order_Item

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, ProductSerializer
from django.shortcuts import get_object_or_404

def get_products(request):
    products = Product.objects.all()
    product_list = list(products.values())
    return JsonResponse(product_list, safe=False)

def get_product(request, id):
    product = get_object_or_404(Product, product_id=id)
    product_data = {
        'id': product.product_id,
        'name': product.name,
        'category': product.category,
        'description': product.description,
        'image_url': product.image_url,
        'price': product.price,
        'sub_description': product.sub_description
    }
    return JsonResponse(product_data, safe=False)

def get_orders(request):
    orders = Order.objects.prefetch_related('order_items__product').all()
    data = []

    for order in orders:
        order_data = {
            'order_id': order.order_id,
            'customer_name': order.customer_name,
            'order_date': order.order_date,
            'total_amount': order.total_amount,
            'phone_number': order.phone_number,
            'email': order.email,
            'delivery_method': order.delivery_method,
            'address': order.address,
            'city': order.city,
            'region': order.region,
            'payment_methods': order.payment_methods,
            'additional_info': order.additional_info,
            'notifications': order.notifications,
            'is_completed': order.is_completed,
            'items':[
                {
                    'product_name': item.product.name,
                    'product_price': float(item.product.price),
                    'quantity': item.quantity,
                    'selected_option': item.selected_option,
                }
                for item in order.order_items.all()
            ]
        }
        data.append(order_data)
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response({'message:': 'Order placed succesfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def put_order(request, id):
    try:
        order = Order.objects.get(order_id = id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    order.is_completed = 'yes'
    order.save()
    serializer =  OrderSerializer(order)
    return Response({'message:': 'Order edited succesfully'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_product(request, id):
    try:
        product = Product.objects.get(product_id = id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def edit_product(request, id):
    try:
        product = Product.objects.get(product_id = id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)