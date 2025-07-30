from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, ProductSerializer

# === TEMPLATE VIEWS (for rendering HTML pages) ======================================

class HomeView(TemplateView):
    template_name = 'shop/index.html'

class PreteensView(TemplateView):
    template_name = 'shop/preteens.html'

class TeensView(TemplateView):
    template_name = 'shop/teens.html'

class NewArrivalsView(TemplateView):
    template_name = 'shop/newarrivals.html'

class BlogView(TemplateView):
    template_name = 'shop/blog.html'

class AboutView(TemplateView):
    template_name = 'shop/about.html'

class HelpView(TemplateView):
    template_name = 'shop/help.html'

class CartPageView(TemplateView):
    template_name = 'shop/cart.html'

# --- Product ViewSet (For listing products) ---
# A ReadOnlyModelViewSet is a simple way to allow 'read-only' access to the product list
class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# --- Helper function to get/create a user's cart ---
# This function contains the logic for managing anonymous user sessions
def get_cart(request):
    cart_id = request.session.get('cart_id')
    cart = None

    if cart_id:
        try:
            cart = Cart.objects.prefetch_related('items__product').get(id=cart_id)
        except Cart.DoesNotExist:
            # The cart_id from the session is invalid so create a new one
            pass

    if not cart:
        cart = Cart.objects.create()
        # Save the new cart's ID into the session for future requests
        request.session['cart_id'] = str(cart.id)
    
    return cart

# --- API Views for Specific Cart Actions ---

class CartView(APIView):
    """View to get the current user's cart."""
    def get(self, request, *args, **kwargs):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    """View to add an item to the cart or increment its quantity."""
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Find an existing item for this product in this cart/create a new one
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            # If the item already existed, just increment its quantity
            cart_item.quantity += 1
        
        cart_item.save()
        
        request.session.modified = True
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveFromCartView(APIView):
    """View to completely remove an item from the cart."""
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        item_id = request.data.get('item_id')

        if not item_id:
            return Response({'error': 'Cart Item ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Ensure the item belongs to the user's current cart
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            request.session.modified = True
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found in your cart'}, status=status.HTTP_404_NOT_FOUND)