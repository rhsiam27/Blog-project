from django.db import models

# Create your models here.
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from . managers import UserManager
class User(AbstractBaseUser,PermissionsMixin):
           username = models.CharField(
                   max_length = 150,
                   validators = [UnicodeUsernameValidator,],
                   unique = True,
           )
           email = models.EmailField(
                   max_length = 150,
                   unique = True,
           )
           objects = UserManager()
           is_staff = models.BooleanField(default=False)
           is_superuser = models.BooleanField(default=False)
           is_active = models.BooleanField(default=True)
           date_joined = models.DateTimeField(auto_now_add=True)
           USERNAME_FIELD = "username"
           #REQUIRED_FIELDS attribute is a list of (optional) fields required when creating a superuser using the createsuperuser management command.
           REQUIRED_FIELDS = ['email',]

           class Meta:
                   ordering = ["-date_joined"]