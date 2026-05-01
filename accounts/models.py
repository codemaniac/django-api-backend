from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return self.user.email
