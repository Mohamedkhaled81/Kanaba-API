"""This is Core models"""
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class KanabaUserManager(BaseUserManager):
    """Kanaba User Manager"""
    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError("Email Should not be empty!")
        if not password:
            raise ValueError("Password should be given!")

        email = KanabaUserManager.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        super_user = self.create_user(email, password, **other_fields)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.role = Role.ADMIN
        super_user.save(using=self._db)
        return super_user


class Role(models.TextChoices):
    ADMIN = "ADMIN", 'Admin'
    CUSTOMER = "CUSTOMER", "Customer"
    TENANT = "TENANT", "Tenant"
    DESIGNER = "DESIGNER", "Designer"


class KanabaUser(AbstractBaseUser, PermissionsMixin):
    """Kanaba User mdoel"""
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug_name = models.SlugField()
    role = models.CharField(choices=Role.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = KanabaUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.slug_name = slugify(f"{self.first_name} {self.last_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.user_id}"
