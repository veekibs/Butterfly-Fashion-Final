# in shop/models.py

from django.db import models
import uuid

# ====================================================================================
# === PRODUCT MODEL ================================================================
# ====================================================================================
# Represents a single product that can be sold in the store
class Product(models.Model):
    # A simple text field for the product's name
    name = models.CharField(max_length=255)
    
    # A larger text field for a detailed description
    description = models.TextField(blank=True, null=True)
    
    # A decimal field for currency, which prevents floating-point rounding errors
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # A field to store the path or URL to the product's image
    image_url = models.CharField(max_length=1024)
    
    # A field to define the main age category. 'choices' creates a dropdown menu in the admin panel
    category = models.CharField(max_length=50, choices=[('preteen', 'Preteen'), ('teen', 'Teen')])
    
    # A boolean (True/False) flag to easily filter for new arrivals
    is_new_arrival = models.BooleanField(default=False)
    
    # An inner class using TextChoices to create clean, readable options for the sub_category field
    class SubCategory(models.TextChoices):
        TOP = 'top', 'Top'
        BOTTOM = 'bottom', 'Bottom'
    
    # A field for the product's type, using the choices defined above
    sub_category = models.CharField(
        max_length=50,
        choices=SubCategory.choices,
        default=SubCategory.TOP, 
    )

    # Defines the human-readable name for a Product instance, used in the Django admin
    def __str__(self):
        return self.name

# ====================================================================================
# === CART MODELS ==================================================================
# ====================================================================================

# Represents a single, anonymous shopping cart session
class Cart(models.Model):
    # A universally unique identifier (UUID) is used as the primary key
    # This is a secure, random ID, perfect for anonymous carts
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    
    # A timestamp that is automatically set only when a cart is first created
    created_at = models.DateTimeField(auto_now_add=True)

    # The string representation for a Cart instance in the admin will be its unique ID
    def __str__(self):
        return str(self.id)

# Represents a single line item within a Cart 
class CartItem(models.Model):
    # A many-to-1 relationship linking this item to a single Cart
    # on_delete=models.CASCADE means if a Cart is deleted, all its items are also deleted automatically
    # related_name='items' is a shortcut that lets us easily get all items from a cart (e.g., my_cart.items.all())
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    
    # A many-to-1 relationship linking this item to a single Product
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    
    # An integer to store how many of this specific product are in the cart
    # PositiveIntegerField ensures the quantity cannot be a negative number
    quantity = models.PositiveIntegerField(default=1)

    # Creates a descriptive name for the cart item instance
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"