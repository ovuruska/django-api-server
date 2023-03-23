from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from scheduling.serializers.auth import CreateUserSerializer

from django.test import TestCase
from django.contrib.auth.models import User
from knox.models import AuthToken

from common.roles import Roles
from scheduling.models import Employee

class AuthTestCase(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.employee = Employee.objects.create(name='John Doe', email='john@example.com', role=Roles.EMPLOYEE_FULL_GROOMING)
        self.user = User.objects.create_user(
            username = 'testuser',
            password='testpassword'
        )
        self.employee.user = self.user
        self.employee.save()
        # Login
        self.token_instance, self.token = AuthToken.objects.create(self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}



class RegisterAPIViewTest(AuthTestCase):

        def test_register_user(self):
            data = {
                "username": "testuser1",
                "password": "testpassword",
            }
            response = self.client.post('/api/authorization/register', data=data, format="json", **self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
