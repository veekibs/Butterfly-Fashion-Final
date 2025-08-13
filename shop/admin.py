# Import the necessary tools from Django + all the models from the models.py file
from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

# --- Product Admin ---
# This class customises how the Product model is displayed in the Django Admin panel
class ProductAdmin(admin.ModelAdmin):
    # list_display controls which fields are shown in the main list view
    list_display = ('name', 'price', 'category', 'sub_category', 'is_new_arrival', 'is_featured')
    # list_filter adds a sidebar to filter the products by these fields
    list_filter = ('category', 'sub_category', 'is_new_arrival', 'is_featured')
    # search_fields adds a search bar to search by product name + description
    search_fields = ('name', 'description')

# --- Cart Admin ---
# This class defines how CartItems should be displayed "inline" within the Cart admin page
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0 # Tells Django not to show extra empty rows for adding new items

# This class customises the main Cart model display
class CartAdmin(admin.ModelAdmin):
    # 'inlines' tells the Cart admin to include the CartItemInline,
    # allowing me to see + edit a cart's items directly on the cart page
    inlines = [CartItemInline]
    list_display = ('id', 'created_at')

# --- Order Admin ---
# This class defines how OrderItems should be displayed "inline" within the Order admin page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# This class customises the main Order model display
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'first_name', 'last_name', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')

# --- Register all models with the admin site ---
# Tell Django to make each model manageable in the admin panel,
# optionally associating them with their custom admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)