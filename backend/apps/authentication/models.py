from django.contrib.auth.models import PermissionsMixin, User, AbstractBaseUser, BaseUserManager
from django.db import models

from apps.teachers.models import Auditorium


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('teacher', 'Преподаватель'),
        ('none', 'Ваша роль не подтверждена'),
    )
    username = None  # отключаем username

    first_name = models.CharField(max_length=50, blank=True, null=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES, default='none', blank=True)
    is_verified = models.BooleanField(default=False)

    available_auditoriums = models.ManyToManyField('Auditorium', blank=True)
    booking_limit = models.PositiveIntegerField(blank=True, null=True)

    is_staff = models.BooleanField(default=False)  # нужно для админки
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


class VerifyCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
