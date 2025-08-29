# --- Imports ---
# Import necessary classes AND functions from Django + Django REST Framework
from django.db.models import Q
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Cart, CartItem, Product, OrderItem, Order
from .serializers import CartSerializer, ProductSerializer, OrderSerializer
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F 

# --- TEMPLATE VIEWS ---
# These views are simple + their only job is to render a specific HTML template

class HomeView(TemplateView):
    template_name = 'shop/index.html'
    # get_context_data sends extra information to the template
    # Here, it's used to tell the navbar which link should be 'active'
    def get_context_data(self, **kwargs):
        return {'page_name': 'home'}

class PreteensView(TemplateView):
    template_name = 'shop/preteens.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'shop'}

class TeensView(TemplateView):
    template_name = 'shop/teens.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'shop'}

class NewArrivalsView(TemplateView):
    template_name = 'shop/newarrivals.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'shop'}

class BlogView(TemplateView):
    template_name = 'shop/blog.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'blog'}

class AboutView(TemplateView):
    template_name = 'shop/about.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'about'}

class HelpView(TemplateView):
    template_name = 'shop/help.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'help'}

class CartPageView(TemplateView):
    template_name = 'shop/cart.html'
    def get_context_data(self, **kwargs):
        return {'page_name': 'cart'}

class CheckoutPageView(TemplateView):
    template_name = 'shop/checkout.html'

class OrderCompleteView(TemplateView):
    template_name = 'shop/ordercomplete.html'
    
    # This function gets the ID of the most recent order from the user's session
    # and passes it to the template, so we can show the "Create Account" form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('last_order_id')
        if order_id:
            context['order_id'] = order_id
        return context
    
class RegisterPageView(TemplateView):
    template_name = 'shop/register.html'

class LoginPageView(TemplateView):
    template_name = 'shop/login.html'

# LoginRequiredMixin is a security feature that automatically redirects
# non-logged-in users to the login page
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch orders where either:
        # 1. user is linked to the current user, OR
        # 2. the email matches the current user's email
        orders = Order.objects.filter(
            Q(user=self.request.user) | Q(email=self.request.user.email)
        ).annotate(
            total_cost=Sum(F('items__quantity') * F('items__price'))
        ).order_by('-created_at')
        
        context['orders'] = orders
        context['page_name'] = 'dashboard'
        return context

# --- API VIEWS (for handling data requests) ---

# --- Product API ---
# A ReadOnlyModelViewSet provides a simple, read-only API endpoint to list all products
class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# --- Cart Helper Function ---
# A reusable function to get the current user's cart from their session/create a new one
def get_cart(request):
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        try:
            # prefetch_related is a performance optimization for the database query
            cart = Cart.objects.prefetch_related('items__product').get(id=cart_id)
        except Cart.DoesNotExist:
            pass # The cart_id in the session is invalid, so create a new cart
    if not cart:
        cart = Cart.objects.create()
        request.session['cart_id'] = str(cart.id)
    return cart

# --- Cart API Views ---
# These views are simple + handle one specific action each
class CartView(APIView):
    """Handles GET requests to fetch the current user's cart"""
    def get(self, request, *args, **kwargs):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    """Handles POST requests to add an item to the cart"""
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # get_or_create finds an existing item/creates a new one
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            # If the item already existed, just increment its quantity
            cart_item.quantity += 1
        cart_item.save()
        request.session.modified = True # Mark the session as modified to ensure it saves
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveFromCartView(APIView):
    """Handles POST requests to remove an item from the cart"""
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        item_id = request.data.get('item_id')
        if not item_id:
            return Response({'error': 'Cart Item ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            request.session.modified = True
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found in your cart'}, status=status.HTTP_404_NOT_FOUND)
        
class CheckoutView(APIView):
    """Handles POST requests to process the final checkout"""
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        if not cart.items.exists():
            return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Create order, attach logged-in user if authenticated
            user = request.user if request.user.is_authenticated else None
            order = serializer.save(user=user)

            # Optional: attach any past orders with the same email to this user
            if user:
                Order.objects.filter(user__isnull=True, email=order.email).update(user=user)

            # Move items from cart to permanent OrderItems
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )

            # Clear cart session
            cart.delete()
            request.session.pop('cart_id', None)
            request.session['last_order_id'] = order.id

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateAccountView(APIView):
    """Handles POST requests to create a user account from a completed order"""
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        password = request.data.get('password')

        if not order_id or not password:
            return Response({'error': 'Order ID and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Invalid order ID.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if an account already exists with the order's email
        if User.objects.filter(email=order.email).exists():
            return Response({'error': 'An account with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user with the details from the order
        user = User.objects.create_user(
            username=order.email,
            email=order.email,
            password=password,
            first_name=order.first_name,
            last_name=order.last_name
        )

        # Link **all previous orders** with this email to the new user
        link_orders_to_user(user)

        return Response({'success': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
    

def link_orders_to_user(user):
    """
    Link all orders that match the user's email but don't have a user assigned yet.
    """
    unlinked_orders = Order.objects.filter(user__isnull=True, email=user.email)
    for order in unlinked_orders:
        order.user = user
        order.save()