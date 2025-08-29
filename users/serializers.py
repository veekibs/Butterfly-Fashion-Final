# Import necessary modules from Django's authentication system + the REST Framework
from django.contrib.auth.models import User
from rest_framework import serializers

# --- User Serializer ---
# This serializer is used to safely display user information
# It intentionally excludes sensitive data like the password hash
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # The fields to include in the JSON output
        fields = ['id', 'username', 'first_name', 'last_name']

# --- Registration Serializer ---
# This serializer is used specifically for creating new users
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        # 'extra_kwargs' allows us to set special properties for certain fields
        # 'write_only': True ensures that the password is used for creation but is NEVER sent back in an API response
        extra_kwargs = {'password': {'write_only': True}}

    # The create method is overridden to handle password hashing
    def create(self, validated_data):
        # Use Django's 'create_user' helper function, which automatically
        # hashes the password before saving it to the database
        user = User.objects.create_user(
            validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user