# in butterfly_api/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This connects all requests starting with 'api/' to the shop app's URLs
    path('api/', include('shop.urls')),
]