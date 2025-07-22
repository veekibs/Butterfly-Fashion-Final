# in shop/admin.py

from django.contrib import admin
from .models import Product, Cart, CartItem

# This class customises how the Product list appears in the admin panel
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'sub_category', 'is_new_arrival')
    list_filter = ('category', 'sub_category', 'is_new_arrival')
    search_fields = ('name', 'description')

# This class tells Django to show CartItems "inside" the Cart detail page
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0 # Don't show extra empty rows to add new items

# This class customises the Cart list view in the admin panel
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('id', 'created_at')

# Tell the admin site about the models and their custom views
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)