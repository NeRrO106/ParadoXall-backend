from django.http import JsonResponse
from .models import Product, Order, Order_Item

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer

from django.core.mail import send_mail
from django.conf import settings

def get_products(request):
    products = Product.objects.all()
    product_list = list(products.values())
    return JsonResponse(product_list, safe=False)

def send_order_to_restaurant(order_data):
    subject='O noua comanda'
    message=f"""
        O noua comanda a fost plasata:
        - Nume client: {order_data['customer_name']}
        - Telefon: {order_data['phone_number']}
        - Metoda de livrare: {order_data['delivery_methods']}
        - Adresa: {order_data.get('address', 'N/A')}
        - Oras: {order_data.get('city', 'N/A')}
        - Judet: {order_data['region']}
        - Metoda de plata: {order_data['payment_methods']}
        - Informatii suplimentare: {order_data.get('additional_info', 'N/A')}

        Produse comandate:    
    """
    total_price = 0

    for item in order_data['order_items']:
        product = Product.objects.get(pk=item['product'])
        item_name = product.name
        item_price = product.price
        item_total = item_price * item['quantity']
        total_price += item_total

        message += f"- Produs: {item_name},{item['selected_option']}, \nCantitate: {item['quantity']}, Pret: {item_price} lei,\n"   

    message += f"\nTotal comanda: {total_price} lei"

    restaurant_email = 'andreilimit66@gmail.com'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [restaurant_email],
        fail_silently=False,
    )

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()

        send_order_to_restaurant(request.data)

        return Response({'message:': 'Order placed succesfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

