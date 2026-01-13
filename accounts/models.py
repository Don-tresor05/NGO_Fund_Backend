from django.db import models

import uuid
from datetime import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self,email, first_name, last_name, password=None, **extra_fields):

        User = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        User.set_password(password)
        User.save(using=self.db)
        return User
    

    def create_superuser(
            self, email, first_name, last_name,password, **extra_fields
    ):
        
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=User.ADMIN,
            password=password,
            **extra_fields
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user
    
class User(AbstractUser, PermissionsMixin):
    ADMIN = 'ADMIN'
    FINANCE = 'FINANCE'
    AUDITOR = 'AUDITOR'
    DONOR = 'DONOR'

    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (FINANCE, 'Finance'),
        (AUDITOR, 'Auditor'),
        (DONOR, 'Donor'),
    ]
    
    username = None
    # Primary key as UUID
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    # Unique email field
    email = models.EmailField(_('email address'), unique=True)
    # First name field with max length of 30 characters
    first_name = models.CharField(max_length=30)
    # Last name field with max length of 30 characters
    last_name = models.CharField(max_length=30)
    # Phone number field unique with exactly 15 characters
    phone_number = models.CharField(
        ("phone number"), max_length=15, unique=True, validators=[
            MinLengthValidator(15),
            MaxLengthValidator(15)
        ]
    )
    # User type field with choices
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default=DONOR
    )
    # Active and staff status fields
    is_active = models.BooleanField(_("is active"), default=True)
    # Staff status field
    is_staff = models.BooleanField(_("staff"),default=False)
    # Date joined field
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    # Use custom user manager
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        return self.first_name
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser


class VerificationCode(models.Model):
    SIGNUP = 'SIGNUP'
    PASSWORD_RESET = 'PASSWORD_RESET'
    VERIFICATION_TYPE_CHOICES = [
        (SIGNUP, 'Signup'),
        (PASSWORD_RESET, 'Password Reset'),
        ('CHANGE_EMAIL', 'Change Email')
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    
    code = models.CharField(max_length=6, blank=True, null=True)
    is_pending = models.BooleanField(default=True)
    label = models.CharField(max_length=100, choices=VERIFICATION_TYPE_CHOICES, default=SIGNUP)
    email = models.EmailField(max_length=254, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    verification_type = models.CharField(
        max_length=20, choices=VERIFICATION_TYPE_CHOICES, default=SIGNUP)
    

    class Meta:
        unique_together = ('user', 'verification_type', 'code')

    @property
    def valid(self):
        future_time = self.joined_at + settings.VERIFICATION_CODE_LIFETIME
        return datetime.now(datetime.timezone.utc) < future_time and self.is_pending

        
        


    