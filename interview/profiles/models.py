from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from typing import Any


class ProfileUserManager(BaseUserManager):
    """
    Custom user ProfileUser model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email: str, password: str, **extra_fields: Any):
        """
        Create and save a user with the given email and password.
        """

        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


def user_avatar_path(user: "ProfileUser", filename: str) -> str:
    # avatar image will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    return f"user_{user.id}/{filename}" if user.id else f"temp/{filename}"  # type: ignore


class ProfileUser(AbstractUser):
    """
    Custom user model based on AbstractUser model. This model is called ProfileUser to avoid conflict with
    the builtin User model, but it functionally replaces that builtin model. It is recommend that you
    use the get_user_model() method imported from django.contrib.auth to get the user model instead
    of importing it directly.
    """

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=user_avatar_path)  # type: ignore
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ProfileUserManager()  # type: ignore
