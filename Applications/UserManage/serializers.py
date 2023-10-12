from rest_framework import serializers
from .models import CustomUser
from rest_framework.authentication import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import IntegrityError

class UserLoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        exclude = ['password', '']

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
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        if password is not None:
            instance.set_password(password)
            instance.save()

        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('password', 'is_active', 'is_superuser',
                   'is_admin', 'is_staff', 'groups', 'user_permissions')

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active', 'is_staff', 'is_admin', 'is_superuser']

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


