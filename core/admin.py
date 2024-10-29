from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

# Register CustomUser with UserAdmin
admin.site.register(CustomUser, UserAdmin)

# Register Book with custom admin class
@admin.register(Book)
class BookA(admin.ModelAdmin):
    list_display = ('title', 'author')
