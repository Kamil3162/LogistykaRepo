from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import BasePasswordHasher, get_hasher, identify_hasher, PBKDF2PasswordHasher


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name,
                    email, city, phone_number,
                    zip_code, password=None, house_number=None,
                    apartment_number=None, street=None, **extra_fields):

        if not first_name:
            raise ValueError("Please enter you name")
        if not last_name:
            raise ValueError("Please enter you last name")
        if not city:
            raise ValueError("Please enter you city")
        if not email:
            raise ValueError("Please enter you email")
        if not zip_code:
            raise ValueError("Please enter zip code:")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            zip_code=zip_code,
            house_number=house_number,
            apartment_number=apartment_number,
            city=city,
            street=street,
            **extra_fields
        )
        hasher = PBKDF2PasswordHasher()
        password_text = password
        print(password_text)
        hashed_password = hasher.encode(password_text, hasher.salt())
        print(hashed_password)

        user.set_password(password)
        print(get_hasher())
        print(user.password)
        print(identify_hasher(user.password))
        user.save(using=self._db)
        return user

    def create_director(self, first_name, last_name,
                    email, city, phone_number,
                    zip_code, password=None, house_number=None,
                    apartment_number=None, street=None, **extra_fields):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            zip_code=zip_code,
            house_number=house_number,
            apartment_number=apartment_number,
            city=city,
            street=street,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        return user

    def create_admin(self, first_name, last_name,
                    email, city, phone_number,
                    zip_code, password=None, house_number=None,
                    apartment_number=None, street=None, **extra_fields):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            zip_code=zip_code,
            house_number=house_number,
            apartment_number=apartment_number,
            city=city,
            street=street,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        return user