from django.contrib import admin

from .models import Book

@admin.register(Book)
class BookA(admin.ModelAdmin):
    list_display = ('title', 'author')

