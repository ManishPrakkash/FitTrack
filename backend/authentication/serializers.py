"""
Serializers for the authentication app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    """
    class Meta:
        model = Profile
        fields = ['name', 'height', 'weight', 'age', 'gender', 'fitness_goal', 'activity_level']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    profile = ProfileSerializer(read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'date_joined', 'last_login']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password']

    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        name = validated_data.pop('name')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Update the profile name
        user.profile.name = name
        user.profile.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    class Meta:
        model = Profile
        fields = ['height', 'weight', 'age', 'gender', 'fitness_goal', 'activity_level']

    def update(self, instance, validated_data):
        """
        Update and return an existing profile instance.
        """
        instance.height = validated_data.get('height', instance.height)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.fitness_goal = validated_data.get('fitness_goal', instance.fitness_goal)
        instance.activity_level = validated_data.get('activity_level', instance.activity_level)
        instance.save()
        return instance
