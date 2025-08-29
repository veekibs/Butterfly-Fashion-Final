# Import necessary modules from Django for URL routing + the views from this app
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CurrentUserView

# This list maps URL endpoints to their corresponding View classes
urlpatterns = [
    # When a request comes to '/api/auth/register/', it will be handled by RegisterView
    path('register/', RegisterView.as_view(), name='register'),
    # Handles '/api/auth/login/'
    path('login/', LoginView.as_view(), name='login'),
    # Handles '/api/auth/logout/'
    path('logout/', LogoutView.as_view(), name='logout'),
    # Handles '/api/auth/current_user/' to check login status
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
]