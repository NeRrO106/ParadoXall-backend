from django.http import JsonResponse
from .models import Product, Order, Order_Item

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from django.conf import settings

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

        #send_order_to_restaurant(request.data)

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

#def send_order_to_restaurant(order_data):
 #   subject='O noua comanda'

  #  delivery_method_display = 'Ridicare' if order_data['delivery_method'] == 'pickup' else 'Livrare'
  #  delivery_adress_display = 'N/A' if order_data['address'] == 'ridicare' else order_data['address']
  #  delivery_city_display = 'N/A' if order_data['city'] == 'ridicare' else order_data['city']

   # message=f"""
    #    O noua comanda a fost plasata:
     #   - Nume client: {order_data['customer_name']}
      #  - Telefon: {order_data['phone_number']}
       # - Metoda de livrare: {delivery_method_display}
       # - Adresa: {delivery_adress_display}
       # - Oras: {delivery_city_display}
       # - Judet: {order_data['region']}
       # - Metoda de plata: {order_data['payment_methods']}
       # - Informatii suplimentare: {order_data.get('additional_info', 'N/A')}

#        Produse comandate:    
 #   """
  #  total_price = 0

   # for item in order_data['order_items']:
    #    product = Product.objects.get(pk=item['product'])
    #    item_name = product.name
    #    item_price = product.price
    #    item_total = item_price * item['quantity']
    #    total_price += item_total

    #    message += f"     -Produs: {item_name}, {item['selected_option']}, \nCantitate: {item['quantity']}, Pret: {item_price} lei,\n"   

    #message += f"\nTotal comanda: {total_price} lei"

    #restaurant_email = 'andreilimit66@gmail.com'

    """send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [restaurant_email],
        fail_silently=False,
    )"""