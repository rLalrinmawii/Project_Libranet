# user/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Since AbstractUser already has fields for username, password, email, etc., 
    # we'll only define additional fields that are not present in AbstractUser.
    roll_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Optional additional fields based on your requirements
    name = models.CharField(max_length=150, blank=False, verbose_name="Name")
    email = models.EmailField(unique=True, blank=False, verbose_name="Email Address")  # Ensuring the email is unique

    # Django will use the username field for authentication, so we usually don't store passwords directly.
    # Instead, you will set the password using Django's built-in user management.

    def __str__(self):
        return self.username
