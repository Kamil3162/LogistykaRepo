from rest_framework import serializers
from .models import CustomUser
from rest_framework.authentication import authenticate
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

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
    class Meta:
        model = CustomUser
        fields = '__all__'

    def check_data(self, clean_data):
        '''
            request.validated_data - its a clean_data
        '''
        try:
            user = CustomUser.objects.create_user(
                first_name=clean_data['first_name'],
                last_name=clean_data['last_name'],
                email=clean_data['email'],
                password=clean_data['password'],
                phone_number=clean_data['phone_number'],
                zip_code=clean_data['zip_code'],
                house_number=clean_data['house_number'],
                apartment_number=clean_data['apartment_number'],
                city=clean_data['city'],
                street=clean_data['street'],
            )
        except IntegrityError:
            raise IntegrityError("User exists with following data")
        except ValueError:
            raise ValueError("You passed improper data")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

