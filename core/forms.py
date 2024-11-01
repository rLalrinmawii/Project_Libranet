from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'asin', 'isbn10', 'availability', 'author', 'description', 'image_url', 
            'images_count', 'rating', 'reviews_count', 'title', 'categories', 'best_sellers_rank'
        ]
        widgets = {
            'author': forms.TextInput(attrs={'placeholder': 'Comma separated for multiple authors'}),
            'categories': forms.TextInput(attrs={'placeholder': 'Comma separated for multiple categories'}),
            'description': forms.Textarea(),
        }
