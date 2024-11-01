# user/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Since AbstractUser already has fields for username, password, email, etc., 
    # we'll only define additional fields that are not present in AbstractUser.
    
    # New fields for user registration
    roll_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # New fields for first name and last name
    first_name = models.CharField(max_length=150, blank=False, verbose_name="First Name")
    last_name = models.CharField(max_length=150, blank=False, verbose_name="Last Name")
    
    # Combining first name and last name into a full name field
    name = models.CharField(max_length=150, blank=False, verbose_name="Full Name")
    
    email = models.EmailField(unique=True, blank=False, verbose_name="Email Address")  # Ensuring the email is unique

    # Django will use the username field for authentication, so we usually don't store passwords directly.
    # Instead, you will set the password using Django's built-in user management.

    def save(self, *args, **kwargs):
        # Combine first and last names into the name field before saving
        self.name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.username


