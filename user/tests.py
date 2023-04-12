from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpassword'
        )

    def test_profile_created(self):
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.user, self.user, 'Profile not created')
        pass

    def test_profile_avatar(self):
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.avatar, 'avatars/default.png', 'Avatar not set')

    def test_dupplicate_username(self):
        with self.assertRaises(IntegrityError) as context:
            u1 = User.objects.create_user(username='testuser')
            u2 = User.objects.create_user(username='testuser')
            u1.save()
            u2.save()
            self.assertTrue('UNIQUE constraint failed' in str(context.exception))

    def test_password_reset(self):
        pass
