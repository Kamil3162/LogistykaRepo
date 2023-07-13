from rest_framework import serializers
from .models import CustomUser
from rest_framework.authentication import authenticate
from rest_framework.exceptions import ValidationError

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60)
    password = serializers.CharField(max_length=30)

    def check_user(self, clean_data):
        user = authenticate(
            username=clean_data['email'],
            password=clean_data['password']
        )
        if not user:
            raise ValidationError("Improper password or login")
        return user

class UserRegisterSerializer(serializers.ModelSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    pass