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
                    ISBN10=row.get('ISBN10', None),            # From CSV
                    title=row['title'],                        # From CSV
                    author=row.get('brand', 'Unknown'),        # Default to 'Unknown' if not in CSV
                    publisher=row.get('manufacturer', 'Unknown'),  # Default to 'Unknown' if not in CSV
                    publication_date=parse_date(row.get('date_first_available', None)),  # From CSV
                    categories=row.get('categories', 'Uncategorized'),  # Default to 'Uncategorized'
                    final_price=row.get('final_price', 0),     # Default price to 0
                    discount=row.get('discount', '0%'),        # Default discount to '0%'
                    availability=row.get('availability', 'Unknown'),  # Default availability to 'Unknown'
                    description=row.get('description', ''),    # Default description to empty string
                    format=row.get('format', 'Unknown'),       # Default format to 'Unknown'
                    rating=row.get('rating', None),            # From CSV
                    reviews_count=row.get('reviews_count', 0), # Default reviews_count to 0
                    image_url=row.get('image_url', None),      # From CSV
                    availability_status="Available"           # Set availability_status to default
                )
                print(f"Added: {row['title']}")
            except IntegrityError as e:
                print(f"Error adding: {row['title']} - {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    load_books()
