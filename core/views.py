from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Book
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User

# Home page (index)
def index(request):
    return render(request, 'core/index.html')

# Admin login page
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Logs in the user
            return redirect('admin_portal')  # Redirects to the admin portal after successful login
        else:
            messages.error(request, 'Invalid username or password.')  # Show error message if login fails

    return render(request, 'core/admin_login.html')  # Render login page if GET request

# User login page
def user_login(request):
    return render(request, 'core/usr_login.html')

# Admin portal page
def admin_portal(request):
    return render(request, 'core/admin_portal.html')

# User portal page
def user_portal(request):
    return render(request, 'core/user_portal.html')

# Add book page
def add_book(request):
    return render(request, 'core/add_book.html')

# Custom 404 page
def error_404(request, exception):
    return render(request, 'core/404.html')

def buy_book(request):
    # Your logic for handling book purchases
    return render(request, 'core/buy_book.html')

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        print("Logging out user")
        logout(request)
        return redirect('admin_portal')

# User registration
def register(request):
    if request.method == "POST":
        print("Form submitted!")  # Debugging line
        name = request.POST.get('usr_name')
        password = request.POST.get('usr_pass')
        email = request.POST.get('usr_email')

        print(f"Name: {name}, Password: {password}, Email: {email}")  # Debugging line

        try:
            # Create a new user
            user = User.objects.create_user(username=name, password=password, email=email)
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('user_login')  # Redirect to login after successful registration
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            print(f"Exception: {e}")  # Debugging line

    return render(request, 'core/usr_login.html')  # Render the registration page if GET request