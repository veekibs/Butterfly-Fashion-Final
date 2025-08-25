from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Product, Cart, CartItem, Order

# This class will hold all the tests for the Product model
class ProductModelTests(TestCase):

    def test_str_representation(self):
        """
        Tests that the Product model's __str__ method returns the product's name.
        """
        # 1. Create a sample product in the test database
        product = Product.objects.create(name="Cool T-Shirt", price=19.99)
        
        # 2. Check if the string representation of the product is equal to its name
        self.assertEqual(str(product), "Cool T-Shirt")

class CartAPITests(TestCase):

    def setUp(self):
        """Set up a sample product for all tests in this class."""
        self.product = Product.objects.create(name="Test Product", price=10.00)

    def test_add_item_to_cart_successfully(self):
        """
        Tests that a POST request to the 'cart-add' API endpoint
        successfully creates a cart and a cart item.
        """
        # Define the URL for your 'add to cart' API endpoint
        url = reverse('cart-add')
        
        # The data we are sending, simulating a frontend request
        data = {'product_id': self.product.id}

        # Use the test client to make a POST request
        response = self.client.post(url, data, format='json')

        # 1. Check that the API returns a successful status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Check that a Cart has been created in the test database
        self.assertEqual(Cart.objects.count(), 1)
        
        # 3. Check that a CartItem has been created
        self.assertEqual(CartItem.objects.count(), 1)
        
        # 4. Check that the created cart item has the correct product and quantity
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_invalid_product_to_cart(self):
        """
        Tests that the API returns a 404 Not Found error if an
        invalid product ID is sent.
        """
        url = reverse('cart-add')
        # Send a product ID that does not exist (e.g., 999)
        data = {'product_id': 999}

        response = self.client.post(url, data, format='json')

        # Check that the API correctly returns a 404 error
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkout_successfully(self):
        """
        Tests that a POST request to the checkout API creates an Order
        and deletes the original Cart.
        """
        # 1. First, create a cart and add an item to it
        cart = Cart.objects.create()
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        # 2. Store the cart's ID in the test session
        session = self.client.session
        session['cart_id'] = str(cart.id)
        session.save()
        
        # 3. Define the URL and the shipping data
        url = reverse('checkout')
        data = {
            'first_name': 'Eve',
            'last_name': 'Developer',
            'email': 'eve@example.com',
            'address': '123 Code Lane',
            'city': 'London',
            'postcode': 'SW1A 0AA'
        }

        # 4. Make the POST request to the checkout API
        response = self.client.post(url, data, format='json')

        # 5. Assert that the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 6. Assert that an Order has been created
        self.assertEqual(Order.objects.count(), 1)
        
        # 7. Assert that the original Cart has been deleted
        self.assertEqual(Cart.objects.count(), 0)

        # 8. Assert that the Order was created with the correct details
        order = Order.objects.first()
        self.assertEqual(order.first_name, 'Eve')
        self.assertEqual(order.items.count(), 1)