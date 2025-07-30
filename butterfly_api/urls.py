from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import HomeView, NewArrivalsView, PreteensView, TeensView, BlogView, AboutView, HelpView, CartPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('new-arrivals/', NewArrivalsView.as_view(), name='new-arrivals'),
    path('preteens/', PreteensView.as_view(), name='preteens'),
    path('teens/', TeensView.as_view(), name='teens'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('about/', AboutView.as_view(), name='about'),
    path('help/', HelpView.as_view(), name='help'),
    path('cart/', CartPageView.as_view(), name='cart'),

    path('api/', include('shop.urls')),
]

# This line tells Django's development server how to serve the collected static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)