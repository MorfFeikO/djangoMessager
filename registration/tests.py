from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status, serializers

from .models import User
from .serializers import RegistrationSerializer


class UserManagerModelTests(TestCase):
    def setUp(self) -> None:
        self.username = 'test_user'
        self.email = 'test@example.com'
        self.password = 'testingpass'

    def test_create_user_without_username(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username=None,
                email=self.email,
                password=self.password)

    def test_create_user_without_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username=self.username,
                email=None,
                password=self.password)

    def test_create_user_success(self):
        user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)

    def test_create_superuser_without_password(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                username=self.username,
                email=self.email,
                password=None)

    def test_create_superuser_success(self):
        user = User.objects.create_superuser(
            username=self.username,
            email=self.email,
            password=self.password)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.test_user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password='testingpass')

    def test_user__str__(self):
        self.assertEqual(self.test_user.__str__(), self.test_user.email)

    def test_user_get_full_name(self):
        self.assertEqual(self.test_user.get_full_name(), self.test_user.username)

    def test_user_get_short_name(self):
        self.assertEqual(self.test_user.get_short_name(), self.test_user.username)


class RegistrationSerializerTests(TestCase):
    def setUp(self) -> None:
        self.user = User(username='test_user', email='test_user@example.com')
        self.user.__setattr__('password', 'testingpass')

    def test_registration_serializer_validate_method_success(self):
        self.user.__setattr__('password2', 'testingpass')
        serializer = RegistrationSerializer(data=self.user.__dict__)
        serializer.is_valid()
        serializer.save()
        self.assertTrue(serializer.is_valid())

    def test_registration_serializer_validate_method_error(self):
        self.user.__setattr__('password2', 'testingpass2')
        serializer = RegistrationSerializer(data=self.user.__dict__)
        serializer.is_valid()
        self.assertRaises(serializers.ValidationError)


class RegistrationAPIViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.username = 'test_user'
        self.email = 'test@example.com'
        self.password = 'testingpass'
        self.password2 = 'testingpass'

    def test_registration_post_success(self):
        response = self.client.post(reverse('registration:registration'), data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'password2': self.password2
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
