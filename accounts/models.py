from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('commission', 'Komissiya'),
        ('applicant', 'Abituriyent'),
    )

    phone = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name or self.phone} ({self.role})"

class PhoneVerification(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone} - {self.code}"
