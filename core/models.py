from django.db import models

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
        managed = False
