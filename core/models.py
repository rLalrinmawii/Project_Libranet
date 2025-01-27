from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from user.models import CustomUser  # Import only once
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.fields import ArrayField


# CustomUser model inheriting from AbstractUser
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# Profile model extending CustomUser with additional fields
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    usr_roll = models.CharField(max_length=100)
    usr_dob = models.DateField()

    def __str__(self):
        return self.user.username


# Book model for handling book records
class Book(models.Model):
    asin = models.CharField(max_length=10, primary_key=True)
    isbn10 = models.CharField(max_length=10, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)

    @property
    def is_available(self):
        if self.availability is None:
            return False
        availability_lower = self.availability.lower()
        if "out of stock" in availability_lower:
            return False
        if "only" in availability_lower or "in stock" in availability_lower:
            return True
        if "usually ships" in availability_lower:
            return True
        return False 

    author = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    images_count = models.SmallIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    reviews_count = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    categories = models.TextField(blank=True, null=True)
    best_sellers_rank = models.TextField(blank=True, null=True)
    embedding = ArrayField(models.FloatField(), blank=True, null=True)  # Stores the vector



    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        managed = True


# Bookmark model to save bookmarked books
class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.book.title}"


# BorrowedBook model to track borrowed books
class BorrowedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)  # Allow return_date to be null

    def return_book(self):
        """Marks the book as returned and sets the return date."""
        self.return_date = timezone.now()

    @property
    def is_returned(self):
        """Checks if the book has been returned."""
        return self.return_date is not None

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


# FinalizedBook model to track finalized borrowings
class FinalizedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} finalized {self.book.title}"
    

# core/models.py

from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    finalized = models.BooleanField(default=False)
