from rest_framework import serializers
from .models import User
import bcrypt


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'date_joined']
        read_only_fields = ['id', 'date_joined']

    def create(self, validated_data):
        """Create and return a new user."""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return an existing user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.save()

        return user
