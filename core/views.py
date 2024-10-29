from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Book
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout 
from django.contrib.auth.models import User
from django.core.paginator import Paginator



# Home page displaying books and search functionality
def homepage(request):
    query = request.GET.get('query', '')  # Capture search query if available
    books = Book.objects.all()  # Fetch all books

    # Filter based on search query
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # Paginate results, displaying 20 books per page
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/homepage.html', {'books': page_obj, 'query': query})


#(index)
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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('user_portal')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/usr_login.html')


# Admin portal page
def admin_portal(request):
    return render(request, 'core/admin_portal.html')

# User portal page


# Add book page
def add_book(request):
    return render(request, 'core/add_book.html')

# Custom 404 page
def error_404(request, exception):
    return render(request, 'core/404.html')

def buy_book(request):
    # Your logic for handling book purchases
    return render(request, 'core/buy_book.html')

#class CustomLogoutView(LogoutView):
    #def get(self, request, *args, **kwargs):
        #print("Logging out user")
        #logout(request)
        #return redirect('admin_portal')
    
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

# User registration

