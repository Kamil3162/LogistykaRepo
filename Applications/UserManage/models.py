from django.db import models
from django.contrib.auth.models import (
    AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager)
from .user_manager import CustomUserManager
from .validators import (
    apartment_house_num_validator,
    street_name_validator,
    zip_code_validator
)
# from .management.user_manager import CustomUserManager
from ..ReceivmentManage.models import Receivment
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


    class Meta:
        permissions = [
            ('view_user_details', 'Can view user details'),
            ('view_own_details', 'Can view own user details'),
            ('update_user_details', 'Can update user details'),
            ('update_own_user_details', 'Can update own user details'),
            ('delete_own_account', 'Can delete own account'),
            ('delete_user_account', 'Can delete user account'),
            ('create_user_account', 'Can create user account'),
            ('view_truck_details', 'Can view truck details'),
            ('update_truck_details', 'Can update truck details'),
            ('delete_truck_details', 'Can delete truck'),
            ('create_truck', 'Can delete truck'),
            ('view_semitrailer_details', 'Can view semitrailer details'),
            ('update_semitrailer_details', 'Can update semitrailer details'),
            ('delete_semitrailer_details', 'Can delete semitrailer'),
            ('create_semitrailer', 'Can create semitrailer'),
            ('create_receivment', 'Can create receivment'),
        ]

    def __str__(self):
        # return f"Custom user model {self.first_name} " \
        #        f"{self.last_name} Phone Number {self.phone_number}"
        return f'{self.first_name} {self.last_name}'

    def show_permissions(self):
        return f"Admin:{self.is_admin} Superuser:{self.is_superuser} "\
               f"Staff:{self.is_staff}"

    def all_fields(self):
        return self.clean_fields()

    def can_be_deleted(self, receivments):
        finish_status = Receivment.get_statuses().FINISHED
        return all(receivment.status == finish_status for receivment in receivments)
