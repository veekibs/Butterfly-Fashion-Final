from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import LogoutView 
from shop.views import HomeView, NewArrivalsView, PreteensView, TeensView, BlogView, AboutView, HelpView, CartPageView, CheckoutPageView, OrderCompleteView, RegisterPageView, LoginPageView, DashboardView

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- PAGE URLS ---
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
    path('api/', include('shop.urls')),
    path('api/auth/', include('users.urls')),
]

# This line tells Django's development server how to serve the collected static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)