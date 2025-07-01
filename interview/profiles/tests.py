from django.test import TestCase


from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import user_avatar_path


User = get_user_model()


class ProfileUserTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123")

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_no_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="testuser",
                email="",
                password="testpass123")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="testuser",
            email="admin@example.com",
            password="adminpass")

        self.assertEqual(admin.email, "admin@example.com")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_create_superuser_invalid_flags_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="testuser",
                email="badadmin@example.com",
                password="pass",
                is_staff=False)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="testuser",
                email="badadmin2@example.com",
                password="pass",
                is_superuser=False)

    def test_user_avatar_path_with_user_id(self):
        testuser = User(
            id=42,
            username="testuser",
            email="test@example.com")

        path = user_avatar_path(testuser, "avatar.png")  #type: ignore

        self.assertEqual(path, "user_42/avatar.png")

    def test_user_avatar_path_without_user_id(self):
        testuser = User(
            id=None,
            username="testuser",
            email="test@example.com")

        path = user_avatar_path(testuser, "avatar.png")  #type: ignore

        self.assertEqual(path, "temp/avatar.png")