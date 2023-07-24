from django.test import TestCase, Client
from Applications.UserManage.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from ..serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserRegisterSerializer,
    UserLoginSerializer
)
class UserTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password': 'test',
            'phone_number': '123456789',
            'zip_code': '12-321',
            'house_number': '32',
            'apartment_number': '42',
            'city': 'Lodz',
            'street': 'Podwawelska'
        }
        self.login_data = {
            'emial': 'test@test.com',
            'password': 'test'
        }
        self.client = APIClient()

    def test_user_permission(self):
        user = CustomUser.objects.create_user(**self.data)
        active = user.is_active
        super_user = user.is_superuser
        admin = user.is_admin
        staff = user.is_staff

        self.assertEqual(active, 1)
        self.assertEqual(super_user, 0)
        self.assertEqual(admin, 0)
        self.assertEqual(staff, 0)

    def test_user_login(self):
        url = reverse('token')
        user = CustomUser.objects.create_user(**self.data)
        self.assertEqual(user.is_active, True)

        # now we are creating post to get token
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']

        # validation of get 200 with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('details-user'),
                                   data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_create_permissions(self):
        # first we create instance of our admin user
        user = CustomUser.objects.create_admin(**self.data)

        # check permissions of user
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_director_create_permissions(self):
        # first we create instance of our admin user
        user = CustomUser.objects.create_director(**self.data)

        # check permissions of user
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, True)

    def test_user_serialize(self):
        # first we create instance of our admin user
        user = CustomUser.objects.create_user(**self.data)

        # now define a sheleton of data
        expected_data = self.data
        serializer = UserSerializer(instance=user)
        self.assertTrue(type(expected_data), type(serializer.data))


