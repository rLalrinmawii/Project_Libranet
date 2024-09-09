from django.shortcuts import render
from .models import Book

# Create your views here.


def index(request):
    books = Book.objects.all()[:50]  # Limit the query to the first 50 books
    return render(request, 'core/index.html', {'books': books})