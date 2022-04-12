# from django.test import TestCase, Client
# from django.urls import reverse
#
# from rest_framework import status
#
# from .models import User
# from .serializers import RegistrationSerializer
#
#
# class UserManagerModelTests(TestCase):
#     def setUp(self) -> None:
#         self.username = 'test_user'
#         self.email = 'test@gmail.com'
#         self.password = 'kulopoplaxan'
#
#     def test_create_user_without_username(self):
#         with self.assertRaises(TypeError):
#             User.objects.create_user(
#                 username=None,
#                 email=self.email,
#                 password=self.password)
#
#     def test_create_user_without_email(self):
#         with self.assertRaises(TypeError):
#             User.objects.create_user(
#                 username=self.username,
#                 email=None,
#                 password=self.password)
#
#     def test_create_user_success(self):
#         user = User.objects.create_user(
#             username=self.username,
#             email=self.email,
#             password=self.password)
#         self.assertEqual(user.username, self.username)
#         self.assertEqual(user.email, self.email)
#
#     def test_create_superuser_without_password(self):
#         with self.assertRaises(TypeError):
#             User.objects.create_superuser(
#                 username=self.username,
#                 email=self.email,
#                 password=None)
#
#     def test_create_superuser_success(self):
#         user = User.objects.create_superuser(
#             username=self.username,
#             email=self.email,
#             password=self.password)
#         self.assertEqual(user.username, self.username)
#         self.assertEqual(user.email, self.email)
#
#
# class UserModelTests(TestCase):
#     def setUp(self) -> None:
#         self.test_user = User.objects.create_user(
#             username='test_user',
#             email='user@gmail.com',
#             password='kulopoplaxan')
#
#     def test_user__str__(self):
#         self.assertEqual(self.test_user.__str__(), self.test_user.email)
#
#     def test_user_get_full_name(self):
#         self.assertEqual(self.test_user.get_full_name(), self.test_user.username)
#
#     def test_user_get_short_name(self):
#         self.assertEqual(self.test_user.get_short_name(), self.test_user.username)
#
#
# class RegistrationSerializerTests(TestCase):
#     def setUp(self) -> None:
#         self.user = User(username='test_user', email='test_user@gmail.com')
#         self.user.set_password('kulopoplaxan')
#
#     def test_registration_serializer_create_method_success(self):
#         serializer = RegistrationSerializer(data=self.user.__dict__)
#         serializer.is_valid()
#         serializer.save()
#         self.assertTrue(serializer.is_valid())
#
#
# class RegistrationAPIViewTests(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
#         self.username = 'test_user'
#         self.email = 'test@gmail.com'
#         self.password = 'kulopoplaxan'
#
#     def test_registration_apiview_post_success(self):
#         response = self.client.post(reverse('registration:registration'), data={
#             'username': self.username,
#             'email': self.email,
#             'password': self.password
#         })
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#
# # python manage.py test djWeatherReminder.apps.registration.tests
# # coverage run --source='.' manage.py test djWeatherReminder.apps.registration
# # coverage report -m
