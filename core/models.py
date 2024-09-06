from django.db import models

class Book(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    ISBN10 = models.CharField(max_length=10, null=True, blank=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    categories = models.CharField(max_length=255, null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.CharField(max_length=10, null=True, blank=True)
    availability = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    format = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    reviews_count = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    availability_status = models.CharField(max_length=100, default="Available")


    def __str__(self):
        return self.title
