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

# --- TEMPLATE VIEWS (for rendering HTML pages) ---

class HomeView(TemplateView):
    template_name = 'shop/index.html'
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
    
    # This function gets the order ID from the session + passes it to the template 
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

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch orders for the current user, calculating the total for each
        orders = Order.objects.filter(user=self.request.user).annotate(
            total_cost=Sum(F('items__quantity') * F('items__price'))
        ).order_by('-created_at')
        
        context['orders'] = orders
        context['page_name'] = 'dashboard'
        return context

# --- API VIEWS ---

class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def get_cart(request):
    cart_id = request.session.get('cart_id')
    cart = None
    if cart_id:
        try:
            cart = Cart.objects.prefetch_related('items__product').get(id=cart_id)
        except Cart.DoesNotExist:
            pass
    if not cart:
        cart = Cart.objects.create()
        request.session['cart_id'] = str(cart.id)
    return cart

class CartView(APIView):
    def get(self, request, *args, **kwargs):
        cart = get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        request.session.modified = True
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RemoveFromCartView(APIView):
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
    """View to handle the final checkout process."""
    def post(self, request, *args, **kwargs):
        cart = get_cart(request)
        if not cart.items.exists():
            return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            cart.delete()
            request.session.pop('cart_id', None)
            
            # Saves the new order ID so the next page can use it 
            request.session['last_order_id'] = order.id

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateAccountView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        password = request.data.get('password')
        if not order_id or not password:
            return Response({'error': 'Order ID and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Invalid order ID.'}, status=status.HTTP_404_NOT_FOUND)
        if User.objects.filter(email=order.email).exists():
            return Response({'error': 'An account with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=order.email,
            email=order.email,
            password=password,
            first_name=order.first_name,
            last_name=order.last_name
        )
        order.user = user
        order.save()
        return Response({'success': 'Account created successfully.'}, status=status.HTTP_201_CREATED)