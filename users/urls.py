from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'), # We'll use Django's default for the actual login
    path('logout/', LogoutView.as_view(), name='logout'),
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
]