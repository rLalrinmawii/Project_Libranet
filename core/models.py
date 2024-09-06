from django.db import models

class Book(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    ISBN10 = models.CharField(max_length=20, null=True, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)  # Author of the book
    publisher = models.CharField(max_length=255, null=True, blank=True)  # Publisher name
    publication_date = models.DateField(null=True, blank=True)  # Publication date of the book
    categories = models.TextField(null=True, blank=True)  # Book categories
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Price of the book
    discount = models.CharField(max_length=100, null=True, blank=True)  # Discount applied to the price
    availability = models.CharField(max_length=100, null=True, blank=True)  # Availability status in store
    description = models.TextField(null=True, blank=True)  # Description of the book
    format = models.CharField(max_length=100, null=True, blank=True)  # Format: Hardcover, eBook, etc.
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # Rating of the book
    reviews_count = models.IntegerField(null=True, blank=True)  # Number of reviews
    image_url = models.URLField(null=True, blank=True)  # URL of the book cover image
    availability_status = models.CharField(max_length=50, default="Available")  # Available, Checked Out, Reserved
    due_date = models.DateField(null=True, blank=True)  # Due date for borrowed books
    borrower = models.CharField(max_length=255, null=True, blank=True)  # Name of the user who borrowed the book

    def __str__(self):
        return self.title
