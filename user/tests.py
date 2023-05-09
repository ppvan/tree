from django.contrib.auth.models import User
from django.core import mail
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.
from .models import Profile


class UserTestCase(TestCase):
    def setUp(self):
        pass

    def test_user_created(self):
        user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="testpassword"
        )
        user.save()
        user.refresh_from_db()

        # self.assertEqual(user.username, "testuser", "User not created")
        self.assertFalse(user.username != "testuser", "User not created")
        self.assertEqual(user.email, "test@gmail.com", "Email not set")
        self.assertTrue(user.check_password("testpassword"), "Password not set")
        self.assertFalse(
            user.profile.email_confirmed, "User active before email confirmation"
        )
        self.assertFalse(user.is_staff, "User is staff on normal creation")

    def test_profile_created(self):
        user = User.objects.create_user(
            username="testprofile", email="test@gmail.com", password="testpassword"
        )
        user.refresh_from_db()
        self.assertEqual(user.profile.user, user, "Profile not created")
        pass

    def test_profile_avatar(self):
        user = User.objects.create_user(
            username="testavatar", email="test@gmail.com", password="testpassword"
        )
        user.refresh_from_db()
        self.assertEqual(user.profile.avatar, Profile.DEFAULT_AVATAR, "Avatar not set")

    def test_dupplicate_username(self):
        with self.assertRaises(IntegrityError) as context:
            u1 = User.objects.create_user(username="testuser")
            u2 = User.objects.create_user(username="testuser")
            u1.save()
            u2.save()
            self.assertTrue("UNIQUE constraint failed" in str(context.exception))


class AuthTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="testpassword"
        )

    def test_login_if_user_not_activated(self):
        response = self.client.post(
            "/user/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302, "Login failed")

    def test_login_if_user_activated(self):
        """Test login if user email is activated"""
        self.user.is_active = True
        self.user.profile.email_confirmed = True
        self.user.save()
        response = self.client.post(
            "/user/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
        # User should be redirected to home page
        self.assertEqual(response.url, "/")


class EmailTest(TestCase):
    def test_send_email(self):
        """Test if email system works (external)"""
        mail.send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, "Subject here")


class ProfileTestCase(TestCase):
    pass
