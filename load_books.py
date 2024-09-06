import csv
from core.models import Book  
from django.utils.dateparse import parse_date
from django.db import IntegrityError

file_path = '/Users/sm/Downloads/Amazon_popular_books_dataset.csv'

def load_books():
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                Book.objects.create(
                    asin=row['asin'],
                    ISBN10=row.get('ISBN10', None),
                    title=row['title'],
                    author=row.get('brand', None),  # Assuming 'brand' is the author in the dataset
                    publisher=row.get('manufacturer', None),
                    publication_date=parse_date(row.get('date_first_available', None)),
                    categories=row.get('categories', None),
                    final_price=row.get('final_price', None),
                    discount=row.get('discount', None),
                    availability=row.get('availability', None),
                    description=row.get('description', None),
                    format=row.get('format', None),
                    rating=row.get('rating', None),
                    reviews_count=row.get('reviews_count', None),
                    image_url=row.get('image_url', None),
                    availability_status="Available"  # Set default availability to "Available"
                )
                print(f"Added: {row['title']}")
            except IntegrityError as e:
                print(f"Error adding: {row['title']} - {e}")

if __name__ == "__main__":
    load_books()
