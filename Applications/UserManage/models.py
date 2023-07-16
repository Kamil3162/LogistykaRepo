from django.db import models
from django.contrib.auth.models import (
    AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager)
from .user_manager import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60, unique=True)
    password = models.CharField(max_length=200)
    house_number = models.CharField(max_length=5)
    apartment_number = models.CharField(max_length=5)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    phone_number = models.IntegerField(max_length=9, unique=True)
    zip_code = models.CharField(max_length=6)
    objects = CustomUserManager()

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # return f"Custom user model {self.first_name} " \
        #        f"{self.last_name} Phone Number {self.phone_number}"
        return f'{self.first_name} {self.last_name}'

