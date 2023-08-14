from django.db import models
from django.contrib.auth.models import (
    AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager)
from .user_manager import CustomUserManager
from .validators import (
    apartment_house_num_validator,
    street_name_validator,
    zip_code_validator
)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    AVAILABLE_CHOICES = (
        ('Dostepny', 'Dostepny'),
        ('Zajety', 'Zajety'),
        ('Urlop', 'Urlop'),
        ('Inne', 'Inne')
    )
    first_name = models.CharField(
        max_length=40,
        validators=[street_name_validator]
    )
    last_name = models.CharField(
        max_length=50,
        validators=[street_name_validator]
    )
    email = models.EmailField(max_length=60, unique=True)
    password = models.CharField(max_length=200)
    house_number = models.CharField(
        max_length=5,
        validators=[apartment_house_num_validator]
    )
    apartment_number = models.CharField(
        max_length=5,
        validators=[apartment_house_num_validator]
    )
    city = models.CharField(
        max_length=30,
        validators=[street_name_validator]
    )
    street = models.CharField(
        max_length=30,
        validators=[street_name_validator]
    )
    phone_number = models.IntegerField(max_length=9, unique=True)
    zip_code = models.CharField(
        max_length=6,
    )
    avaiable = models.CharField(
        max_length=8,
        choices=AVAILABLE_CHOICES,
        default='Dostepny'
    )
    own_car = models.BooleanField(blank=False, default=False)

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

    def show_permissions(self):
        return f"Admin:{self.is_admin} Superuser:{self.is_superuser} "\
               f"Staff:{self.is_staff}"

    def all_fields(self):
        return self.clean_fields()

    # def get_all_permissions(self, obj=None):
    #     pass
    #
    # def get_user_permissions(self, obj=None):
    #     pass
    #
    # def has_perm(self, perm, obj=None):
    #     pass
