from django.test import TestCase, Client
from django.urls import reverse

from rest_framework.test import APIRequestFactory

from registration.models import User

from .models import Message
from .utils import success_response, repeated_action_response
from . views import UserViewSet, MessageViewSet


factory = APIRequestFactory()


def create_test_user(username):
    user = User.objects.create_user(
        username=f'{username}',
        email=f'{username}@example.com',
        # password=f'{username}pass'
    )
    user.set_password(f'{username}pass')
    user.save()
    return user


class ProfileModelTests(TestCase):
    def setUp(self) -> None:
        self.main_user = create_test_user(username='user-1')
        self.support_user = create_test_user(username='user-2')

    def test_main_user_is_follow_return_false(self):
        self.main_user.profile.follows.add(self.support_user)
        self.assertTrue(self.main_user.profile.is_follow(self.support_user))

    def test_main_user_is_follow_return_true(self):
        self.assertFalse(self.main_user.profile.is_follow(self.support_user))

    def test_profile__str__(self):
        self.assertEqual(self.main_user.__str__(), self.main_user.email)


class MessageModelTests(TestCase):
    def setUp(self) -> None:
        self.main_user = create_test_user(username='user-1')
        self.message = Message(owner=self.main_user, body='111')
        self.message.save()

    def test_message_liked_by_return_false(self):
        self.message.liked_by.add(self.main_user)
        self.assertTrue(self.message.is_liked_by(self.main_user))

    def test_main_user_is_follow_return_true(self):
        self.assertFalse(self.message.is_liked_by(self.main_user))

    def test_profile__str__(self):
        self.assertEqual(
            self.message.__str__(),
            f'Message -> {self.main_user.username}-{self.message.created_at}'
        )


class UtilsTests(TestCase):
    def setUp(self) -> None:
        self.name = 'name'

    def test_response_status_200(self):
        self.assertEqual(success_response(self.name).status_code, 200)
        self.assertEqual(
            success_response(self.name).data,
            {'name': 'Success.'}
        )

    def test_response_status_403(self):
        self.assertEqual(repeated_action_response(self.name).status_code, 400)
        self.assertEqual(
            repeated_action_response(self.name).data,
            {'name': 'The action was previously performed.'}
        )


class UserViewSetTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.main_user = create_test_user(username='user-11')
        self.support_user = create_test_user(username='user-22')
        self.client.login(username='user-11@example.com',
                          password='user-11pass')

    def test_follow_not_followed_user(self):
        response = self.client.get(reverse(
            'user-follow',
            args=[self.support_user.id])
        )
        self.assertEqual(200, response.status_code)

    def test_follow_the_followed_user(self):
        self.main_user.profile.follows.add(self.support_user)
        self.support_user.profile.followers.add(self.main_user)
        response = self.client.get(reverse(
            'user-follow',
            args=[self.support_user.id])
        )
        self.assertEqual(400, response.status_code)

    def test_unfollow_not_followed_user(self):
        response = self.client.get(reverse(
            'user-unfollow',
            args=[self.support_user.id])
        )
        self.assertEqual(400, response.status_code)

    def test_unfollow_the_followed_user(self):
        self.main_user.profile.follows.add(self.support_user)
        self.support_user.profile.followers.add(self.main_user)
        response = self.client.get(reverse(
            'user-unfollow',
            args=[self.support_user.id])
        )
        self.assertEqual(200, response.status_code)


class MessageViewSetTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.main_user = create_test_user(username='user-11')
        self.message = Message(owner=self.main_user, body='111')
        self.message.save()
        self.client.login(username='user-11@example.com',
                          password=f'user-11pass')

    def test_like_not_liked_message(self):
        response = self.client.get(reverse(
            'message-like',
            args=[self.message.id])
        )
        self.assertEqual(200, response.status_code)

    def test_like_the_liked_message(self):
        self.message.liked_by.add(self.main_user)
        response = self.client.get(reverse(
            'message-like',
            args=[self.message.id])
        )
        self.assertEqual(400, response.status_code)

    def test_dislike_not_liked_message(self):
        response = self.client.get(reverse(
            'message-dislike',
            args=[self.message.id])
        )
        self.assertEqual(400, response.status_code)

    def test_dislike_liked_message(self):
        self.message.liked_by.add(self.main_user)
        response = self.client.get(reverse(
            'message-dislike',
            args=[self.message.id])
        )
        self.assertEqual(200, response.status_code)

    def test_create_message(self):
        response = self.client.post(reverse('message-list'), data={'body': '123123'})
        self.assertEqual(201, response.status_code)

