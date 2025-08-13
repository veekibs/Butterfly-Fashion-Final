# Import necessary modules from Django's database library, authentication system + Python's uuid library
from django.db import models
from django.contrib.auth.models import User
import uuid

# --- PRODUCT MODEL ---
# Represents a single product that can be sold in the store
class Product(models.Model):
    # A simple text field for the product's name
    name = models.CharField(max_length=255)

    # A larger text field for a detailed description
    # blank=True AND null=True make it optional
    description = models.TextField(blank=True, null=True)
    
    # A decimal field for currency, which prevents floating-point rounding errors
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # A field to store the path to the product's image
    image_url = models.CharField(max_length=1024)
    
    # NEW FIELD for the hover image 
    model_image_url = models.CharField(max_length=1024, blank=True, null=True)
    
    # A field to define the main category, creating a dropdown in the admin panel
    category = models.CharField(max_length=50, choices=[('preteen', 'Preteen'), ('teen', 'Teen')])
    
    # A boolean (True/False) flag to easily filter for new arrivals
    is_new_arrival = models.BooleanField(default=False)
    
    # A boolean (True/False) flag to easily filter for featured products on the homepage
    is_featured = models.BooleanField(default=False)
    
    # An inner class using TextChoices to create clean, readable options for the sub_category field
    class SubCategory(models.TextChoices):
        TOP = 'tops', 'Tops'
        BOTTOM = 'bottoms', 'Bottoms'
        DRESSES = 'dresses', 'Dresses'
        SETS = 'sets', 'Sets'
    
    # A field for the product's type, using the choices defined above
    sub_category = models.CharField(
        max_length=50,
        choices=SubCategory.choices,
        default=SubCategory.TOP, 
    )

    # Defines the human-readable name for a Product instance, used in the Django admin
    def __str__(self):
        return self.name

# --- CART MODELS ---
# Represents a single, anonymous shopping cart session
class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# Represents a single line item within a Cart
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
# --- ORDER MODELS ---
# Represents a completed customer order
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

# Represents a single product line within a completed Order
class OrderItem(models.Model):
    # on_delete=PROTECT prevents a product from being deleted if it's part of an order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)