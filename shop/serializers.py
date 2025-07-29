# in shop/serializers.py

from rest_framework import serializers
from .models import Product, Cart, CartItem

# ====================================================================================
# === PRODUCT SERIALIZERS ==========================================================

# This serializer is for the main product list page (e.g., /api/products/)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' # Include ALL fields from the Product model

# This is a simpler version used to show product details inside a cart item
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_url']

# === CART SERIALIZERS =============================================================

# A serializer for the CartItem model
class CartItemSerializer(serializers.ModelSerializer):
    # "nest" the SimpleProductSerializer here to show full product details
    product = SimpleProductSerializer(read_only=True)
    # A custom field to calculate the total price for this line item
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

# A serializer for the main Cart model
class CartSerializer(serializers.ModelSerializer):
    # Nest the CartItemSerializer to show a list of all items in the cart
    # 'many=True' tells the serializer to expect a list of items
    items = CartItemSerializer(many=True, read_only=True)
    # A custom field to calculate the grand total for the entire cart
    grand_total = serializers.SerializerMethodField()

    def get_grand_total(self, cart: Cart):
        # Calculate the total by summing up the total_price of each item
        return sum(item.quantity * item.product.price for item in cart.items.all())

    class Meta:
        model = Cart
        fields = ['id', 'items', 'grand_total']