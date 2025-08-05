from django.db import models
from django.contrib.auth.models import User
import uuid

# --- PRODUCT MODEL ---
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=1024)
    # NEW FIELD for the hover image 
    model_image_url = models.CharField(max_length=1024, blank=True, null=True)
    category = models.CharField(max_length=50, choices=[('preteen', 'Preteen'), ('teen', 'Teen')])
    is_new_arrival = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class SubCategory(models.TextChoices):
        TOP = 'tops', 'Tops'
        BOTTOM = 'bottoms', 'Bottoms'
        DRESSES = 'dresses', 'Dresses'
        SETS = 'sets', 'Sets'
    
    sub_category = models.CharField(
        max_length=50,
        choices=SubCategory.choices,
        default=SubCategory.TOP, 
    )

    def __str__(self):
        return self.name

# --- CART MODELS ---
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
# --- ORDER MODELS ---
class Order(models.Model):
    # Optional link to a user account
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    # These are the shipping details for the order
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    charity_choice = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)