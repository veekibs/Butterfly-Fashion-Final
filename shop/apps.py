# Import the base AppConfig class from Django
from django.apps import AppConfig


# This class defines the configuration for the 'shop' application
# Django uses this to know about the app + how it should be handled
class ShopConfig(AppConfig):
    # Sets the default primary key type for models in this app to BigAutoField (a 64-bit integer)
    default_auto_field = 'django.db.models.BigAutoField'
    # The name of the application
    name = 'shop'