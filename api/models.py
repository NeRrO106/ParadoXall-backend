from django.db import models

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default = '')
    category = models.CharField(max_length=50, default='')
    image_url = models.CharField(max_length=255, default='')

    class Meta:
        db_table = 'products'

class Order(models.Model):

    DELIVERY_METHODS = [
        ('delivery', 'La domiciliu'),
        ('pickup', 'Ridicare personala'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Numerar'),
        ('creditCard', 'Card'),
    ]

    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHODS, default='delivery')
    address = models.TextField()
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    payment_methods = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    additional_info = models.TextField(null=True, blank=True);


class Order_Item(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selected_option = models.CharField(max_length=50, null=True, blank=True)

