# Import necessary modules from Django + the REST Framework
from django.contrib.auth import authenticate, login, logout
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from django.shortcuts import redirect
from shop.models import Order 

# --- Registration View ---
# Handles the creation of new user accounts
class RegisterView(APIView):
    # The post method handles POST requests sent to this view
    def post(self, request):
        # Create an instance of the RegisterSerializer with the data from the request
        serializer = RegisterSerializer(data=request.data)
        # Check if the provided data is valid (e.g., email is not already in use)
        if serializer.is_valid():
            # If valid, save the new user to the database
            user = serializer.save()
            # Log the new user in automatically
            login(request, user)
            # Return the new user's data (without the password) + a '201 Created' status
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        # If the data is not valid, return the errors + a '400 Bad Request' status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Login View ---
# Handles user login
class LoginView(APIView):
    # Allow any user (even anonymous ones) to access this view
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Get the username + password from the request data
        username = request.data.get('username') # This will be the user's email
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        # 'authenticate' checks if the provided credentials are valid
        user = authenticate(username=username, password=password)

        # If the user is valid, log them in and create a session
        if user:
            login(request, user)
            # --- LINK PREVIOUS ORDERS TO USER ---
            Order.objects.filter(user__isnull=True, email=user.email).update(user=user)
            # Return the logged-in user's data
            return Response(UserSerializer(user).data)
        
        # If the credentials are invalid, return an error
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# --- Logout View ---
# Handles user logout
class LogoutView(APIView):
    def post(self, request):
        # Django's 'logout' function clears the user's session data
        logout(request)
        # This now tells the browser to redirect to the homepage after logging out
        return redirect('home') 

# --- Current User View ---
# A helper view to check if a user is currently logged in
class CurrentUserView(APIView):
    # The get method handles GET requests
    def get(self, request):
        # Check if the user making the request is authenticated
        if request.user.is_authenticated:
            # If yes, return their user data
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        # If not, return an 'Unauthorized' status
        return Response(status=status.HTTP_401_UNAUTHORIZED)