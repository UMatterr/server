from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  BaseUserManager, PermissionsMixin

from core.models import TimestampModel


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        user = self.model(
            username=username, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimestampModel):

    objects = UserManager()

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # verified_email = models.BooleanField(default=False)
    # verified_phone_number = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = [
        'email', 'password',
    ]

    class Meta:
        db_table = 'user'
