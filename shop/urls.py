from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartView, AddToCartView, RemoveFromCartView, CheckoutView, CreateAccountView

# The router handles the simple product list view
router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

# Define specific + simple paths for the cart actions
urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='cart-remove'),
    # Added the path for the checkout API endpoint 
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('create-account/', CreateAccountView.as_view(), name='create-account'),
]