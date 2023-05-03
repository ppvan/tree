from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        pass

    def test_user_created(self):
        user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="testpassword"
        )
        user.save()
        user.refresh_from_db()

        self.assertEqual(user.username, "testuser", "User not created")
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
        self.assertEqual(user.profile.avatar, "defaults/avatar.png", "Avatar not set")

    def test_dupplicate_username(self):
        with self.assertRaises(IntegrityError) as context:
            u1 = User.objects.create_user(username="testuser")
            u2 = User.objects.create_user(username="testuser")
            u1.save()
            u2.save()
            self.assertTrue("UNIQUE constraint failed" in str(context.exception))
