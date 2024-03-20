"""This is Core models"""
import magic
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


# Custom Validators
def validate_is_legit_pdf(file):
    # file argument is a file object
    accept_mime = 'application/pdf'
    file_type = magic.from_buffer(file.read(1024), mime=True)
    if accept_mime != file_type:
        raise ValidationError("UnSupported file type..")


class UserManager(BaseUserManager):
    """User Manager"""
    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError("Email Should not be empty!")
        if not password:
            raise ValueError("Password should be given!")

        email = UserManager.normalize_email(email)
        user = self.model(email=email.lower(), **other_fields)
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

    def create_staff(self, email, password=None, **other_fields):
        staff_user = self.create_user(email, password, **other_fields)
        staff_user.is_staff = True
        staff_user.role = Role.DESIGNER
        staff_user.save(using=self._db)
        return staff_user


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    CUSTOMER = "CUSTOMER", "Customer"
    TENANT = "TENANT", "Tenant"
    DESIGNER = "DESIGNER", "Designer"


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slug_name = models.SlugField()
    gender = models.CharField(chiocies=Gender.choices, default=None)
    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(choices=Role.choices, default=Role.CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.slug_name = slugify(f"{self.first_name} {self.last_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.user_id}"


class Customer(models.Model):
    """Customer Related Fields"""
    customer_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Customer: {self.user.slug_name}"


class Tenant(models.Model):
    """Tenant Related Fields"""
    tenant_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=10, unique=True)
    slug_brand = models.SlugField()
    trade_license = models.FileField(
        upload_to='license/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_is_legit_pdf
        ])

    def save(self, *args, **kwargs):
        self.slug_brand = slugify(self.brand_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tenant: {self.user.slug_name}, Brand: {self.slug_brand}"
