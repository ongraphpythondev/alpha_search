from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
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
        return self.create(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    MALE, FEMALE = "M", "F"
    GENDER = (
        (MALE, "MALE"),
        (FEMALE, "FEMALE"),
    )

    # username = models.CharField(max_length=100, null=True ,default="")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=256, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=1, default="M")
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=256)
    mobile = models.CharField(max_length=20,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

class JwtToken(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    access_token = models.CharField(max_length=500)
    is_block = models.BooleanField(default=False)