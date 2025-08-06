from django.contrib.auth import authenticate, login, logout
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer
from django.shortcuts import redirect

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username') # This will be the user's email
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return Response(UserSerializer(user).data)
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        # This now tells the browser to redirect to the homepage
        return redirect('home') 

class CurrentUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)