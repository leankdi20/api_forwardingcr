"""
DATABASE MODELS
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import EmailValidator, MinLengthValidator
from django.conf import settings
from django.contrib.auth.password_validation import validate_password

import urllib.parse

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        if password:
            validate_password(password)  # Valida según las políticas de Django
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password) #Hashea el password.
        user.save(using=self._db)
        return user
    
    # setdefault() es un método que se utiliza para obtener el valor de una clave si existe en el diccionario. Si no existe, se inserta la clave con el valor por defecto especificado.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True,validators=[EmailValidator(message="Ingrese un correo válido.")])
    first_name = models.CharField(max_length=30,null=True, blank=True)
    last_name = models.CharField(max_length=30,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email