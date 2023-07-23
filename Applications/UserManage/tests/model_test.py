from django.test import TestCase, Client
from Applications.UserManage.models import CustomUser
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

class UserTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            first_name='test',
            last_name='test',
            email='test@test.com',
            password='test',
            phone_number='123456789',
            zip_code='12-321',
            house_number='32',
            apartment_number='42',
            city='Lodz',
            street='Podwawelska',
        )
        self.client = APIClient()

    def test_user_permission(self):
        active = self.user.is_active
        super_user = self.user.is_superuser
        admin = self.user.is_admin
        staff = self.user.is_staff

        self.assertEqual(active, 1)
        self.assertEqual(super_user, 0)
        self.assertEqual(admin, 0)
        self.assertEqual(staff, 0)

    def test_user_login(self):
        url = reverse('token')
        data = {
            'email': self.user.email,
            'password': self.user.password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)