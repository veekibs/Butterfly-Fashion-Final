from django.contrib import admin
# Import Order + OrderItem
from .models import Product, Cart, CartItem, Order, OrderItem

# --- Product Admin ---
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'sub_category', 'is_new_arrival', 'is_featured')
    list_filter = ('category', 'sub_category', 'is_new_arrival')
    search_fields = ('name', 'description')

# --- Cart Admin ---
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('id', 'created_at')

# --- Order Admin ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'first_name', 'last_name', 'paid', 'created_at')
    list_filter = ('paid', 'created_at')

# --- Register all models ---
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin) # Register Order
admin.site.register(OrderItem) # Register OrderItem