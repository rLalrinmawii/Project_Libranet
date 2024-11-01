from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm
from user.models import CustomUser
from django.db.models import Q
from django.contrib.auth.views import LogoutView 

# List all books as JSON
def list_books(request):
    books = Book.objects.all().values('title', 'author', 'asin', 'rating')
    return JsonResponse(list(books), safe=False)

# Add a new book to the database
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect('admin_portal')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm()
    return render(request, 'core/add_book.html', {'form': form})

# List users with search functionality
def list_users(request):
    search_query = request.GET.get('search', '').strip()  # Retrieve the search parameter
    if search_query:
        users = CustomUser.objects.filter(
            Q(name__icontains=search_query) | Q(roll_number__icontains=search_query),
            is_staff=False
        ).values('id', 'username', 'email', 'name', 'roll_number', 'date_of_birth',
                 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    else:
        users = CustomUser.objects.filter(is_staff=False).values('id', 'username', 'email', 'name', 'roll_number',
                                                                 'date_of_birth', 'is_superuser', 'is_staff', 
                                                                 'is_active', 'date_joined')

    return JsonResponse(list(users), safe=False)

# Homepage view with book listing and pagination
def homepage(request):
    query = request.GET.get('query', '')
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # # Add a welcome message for admin
    # if request.user.is_authenticated:
    #     if request.user.is_superuser:
    #         messages.success(request, "Welcome, Admin!")
    #     else:
    #         messages.success(request, f"Welcome, {request.user.username}!")

    context = {
        'books': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'query': query,
    }

    return render(request, 'core/homepage.html', context)

# Index view
def index(request):
    return render(request, 'core/index.html')

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('admin_portal')  # Redirect to admin portal after login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/admin_login.html')

# Admin portal view
def admin_portal(request):
    return render(request, 'core/admin_portal.html')

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        # Define the redirect URL after logout
        return reverse_lazy('user_login')  # Redirect to the user login page


# Error 404 view
def error_404(request, exception):
    return render(request, 'core/404.html')

def buy_book(request):
    return render(request, 'core/buy_book.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('/')  # Redirect to homepage after successful login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/usr_login.html')  # Return the login template

def user_portal(request):
    if request.user.is_authenticated:
        return render(request, 'core/user_portal.html')  # Render user portal page
    else:
        messages.error(request, "You need to log in to access this page.")
        return redirect('user_login')  # Redirect to login if not authenticated

# Simple logout view
def simple_logout(request):
    logout(request)  # Log out the user
    messages.success(request, "You have been logged out.")  # Optional: success message
    return redirect('user_login')  # Redirect to the login page