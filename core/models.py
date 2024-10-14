from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        # Optionally customize the table name
        # db_table = 'custom_user' 

    # Override groups and user_permissions fields to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Custom related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class Book(models.Model):
    asin = models.CharField(max_length=10, primary_key=True)
    isbn10 = models.CharField(max_length=10, blank=True, null=True)
    availability = models.BooleanField(default=False)
    author = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    images_count = models.SmallIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    reviews_count = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    categories = models.TextField(blank=True, null=True)
    best_sellers_rank = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'
        managed = False  # Set to True if you want Django to manage the database table
