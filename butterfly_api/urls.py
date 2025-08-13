# Import necessary modules from Django for admin, URL routing + settings
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import all the View classes from the apps that will be used to render pages
from users.views import LogoutView 
from shop.views import HomeView, NewArrivalsView, PreteensView, TeensView, BlogView, AboutView, HelpView, CartPageView, CheckoutPageView, OrderCompleteView, RegisterPageView, LoginPageView, DashboardView

# This list holds all the URL patterns for the ENTIRE project
# Django checks each pattern in order from top to bottom
urlpatterns = [
    # The standard URL for the Django admin panel
    path('admin/', admin.site.urls),

    # --- PAGE URLS ---
    # These paths map a URL to a specific TemplateView to render an HTML page
    path('', HomeView.as_view(), name='home'),
    path('new-arrivals/', NewArrivalsView.as_view(), name='new-arrivals'),
    path('preteens/', PreteensView.as_view(), name='preteens'),
    path('teens/', TeensView.as_view(), name='teens'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('about/', AboutView.as_view(), name='about'),
    path('help/', HelpView.as_view(), name='help'),
    path('cart/', CartPageView.as_view(), name='cart'),
    path('checkout/', CheckoutPageView.as_view(), name='checkout-page'),
    path('order-complete/', OrderCompleteView.as_view(), name='order-complete'),
    path('register/', RegisterPageView.as_view(), name='register-page'),
    path('login/', LoginPageView.as_view(), name='login-page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # --- API URLS ---
    # These paths group all the API endpoints together under a prefix
    # 'include' tells Django to look in the specified app's urls.py file for more patterns
    path('api/', include('shop.urls')),
    path('api/auth/', include('users.urls')),
]

# This is a helper for the Django development server
# It should only be used when DEBUG is True (i.e., not in production)
if settings.DEBUG:
    # This line tells the development server how to serve static files (like CSS and JS)
    # that have been gathered by the 'collectstatic' command
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)