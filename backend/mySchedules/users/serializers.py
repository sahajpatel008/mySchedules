from rest_framework import serializers
from .models import User  

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password isn't returned in the response
            'created_at': {'read_only': True},  # `created_at` should be auto-generated
        }

    def create(self, validated_data):
        # Use the `create_user` method to ensure the password is hashed
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
