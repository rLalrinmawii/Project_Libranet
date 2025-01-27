from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Book, Bookmark,BorrowedBook, CartItem
from .forms import BookForm
from user.models import CustomUser
from django.db.models import Q
from django.contrib.auth.views import LogoutView 
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Exists, OuterRef
from django.utils import timezone
from datetime import timedelta
from .models import Book, BorrowedBook, FinalizedBook
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import FinalizedBook
import logging
from .chatbot import BookRecommendationChatbot
from django.core.paginator import Paginator
import warnings
from django.core.paginator import Paginator
from django.core.paginator import UnorderedObjectListWarning 



def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        chatbot = BookRecommendationChatbot(user_input)
        response = chatbot.generate_response()
        # print(response)
        return JsonResponse({"response": response})
    return render(request, 'core/chatbot.html')

@login_required
def borrow_book(request, asin):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to borrow a book.")
        return redirect('index')

    book = get_object_or_404(Book, asin=asin)

    # Check if the book is already in the borrowed cart
    borrowed_book, created = BorrowedBook.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={
            'borrow_date': timezone.now(),
            'return_date': timezone.now() + timedelta(days=14)
        }
    )

    if not created:
        messages.info(request, f"'{book.title}' is already in your cart.")
    else:
        book.save()
        messages.success(request, f"You added '{book.title}' to your cart. Please return by {borrowed_book.return_date.date()}.")

    return redirect('homepage')






@login_required
def borrowed_books_view(request):
    # Fetch both borrowed and finalized books for the user
    borrowed_books = BorrowedBook.objects.filter(user=request.user)
    finalized_books = FinalizedBook.objects.filter(user=request.user)
    
    finalized_count = finalized_books.count()  # Count of finalized books

    context = {
        'borrowed_books': borrowed_books,
        'finalized_books': finalized_books,
        'finalized_count': finalized_count,  # Include count in the context
    }
    
    return render(request, 'core/borrowed_books.html', context)

@login_required
def remove_borrowed_book(request, asin):
    if request.method == "POST":
        try:
            borrowed_book = BorrowedBook.objects.get(user=request.user, book__asin=asin)
            book = borrowed_book.book
            borrowed_book.delete()
            
            book.is_available = True  
            book.save()  # Save availability changes

            messages.success(request, f"'{book.title}' is now available in the library.")
            return JsonResponse({"status": "success"})

        except BorrowedBook.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Book not found"}, status=404)




import logging

logger = logging.getLogger(__name__)

@login_required
def finalize_borrow(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)

    if not borrowed_books:
        messages.error(request, "You have no borrowed books to finalize.")
        return redirect('borrowed_books')  # Redirect to the borrowed books view

    finalized_books_list = []
    for borrowed_book in borrowed_books:
        try:
            finalized_book = FinalizedBook.objects.create(
                user=request.user,
                book=borrowed_book.book,
                borrow_date=borrowed_book.borrow_date,
                return_date=borrowed_book.return_date
            )
            finalized_books_list.append({
                'title': borrowed_book.book.title,
                'borrow_date': borrowed_book.borrow_date.strftime('%Y-%m-%d'),
                'return_date': borrowed_book.return_date.strftime('%Y-%m-%d')
            })
            borrowed_book.delete()
        except Exception as e:
            logger.error(f"Error finalizing book: {e}")

    messages.success(request, "Books have been finalized for borrowing.")
    return redirect('borrowed_books')  # Redirect to the borrowed books view after finalizing






# List all books as JSON
# List all books as JSON
def list_books(request):
    # Ensure the books are ordered before pagination
    books = Book.objects.all().order_by('title').values('title', 'author', 'asin', 'rating')
    paginator = Paginator(books, 20)  # Show 20 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return JsonResponse(list(page_obj), safe=False)


# Suppress the UnorderedObjectListWarning
warnings.filterwarnings("ignore", category=UnorderedObjectListWarning)





# Add a new book to the database
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the book to the Book model
            messages.success(request, "Book added successfully!")
            return redirect('admin_portal')
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # Log form errors for debugging

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


# Homepage view with book listing, pagination, and bookmark status
def homepage(request):
    query = request.GET.get('query', '')
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    # Add bookmark status for each book if user is authenticated
    if request.user.is_authenticated:
        # Use a subquery to check if a bookmark exists for the book and the current user
        bookmarks = Bookmark.objects.filter(user=request.user, book=OuterRef('pk'))
        books = books.annotate(is_bookmarked=Exists(bookmarks))

    # Pagination
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'query': query,
    }

    return render(request, 'core/homepage.html', context)

#the following is for bookmarked books

# @csrf_exempt  # Use this temporarily to ensure CSRF is not blocking DELETE requests
@require_http_methods(["POST", "DELETE"])
def toggle_bookmark(request, book_id):
    # Determine if this is meant to be a DELETE request
    method = request.POST.get('_method', request.method)  # Get '_method' if provided, else use actual method

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if method == 'POST':
        # Add bookmark
        Bookmark.objects.get_or_create(user=request.user, book=book)
        return JsonResponse({'status': 'bookmarked'})

    elif method == 'DELETE':
        # Remove bookmark
        Bookmark.objects.filter(user=request.user, book=book).delete()
        return JsonResponse({'status': 'unbookmarked'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

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

# def buy_book(request):
#     return render(request, 'core/buy_book.html')

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


#for bookmarks


@require_POST
@login_required
def bookmark_book(request, asin):
    book = get_object_or_404(Book, asin=asin)

    if request.user.is_staff:
        return JsonResponse({'error': 'Staff members cannot bookmark books.'}, status=403)

    # Create a new bookmark or delete existing one
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, book=book)
    if created:
        return JsonResponse({'status': 'bookmarked'})
    else:
        # If already bookmarked, remove it
        bookmark.delete()
        return JsonResponse({'status': 'unbookmarked'})

@require_http_methods(["DELETE"])
@login_required
def remove_bookmark(request, asin):
    book = get_object_or_404(Book, asin=asin)
    bookmark = Bookmark.objects.filter(user=request.user, book=book).first()
    
    if bookmark:
        bookmark.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'error': 'not found'}, status=404)



@login_required  # Only accessible to logged-in users
def bookmarked_books(request):
    # Fetch all books bookmarked by the current user
    bookmarked_books = Book.objects.filter(bookmark__user=request.user)

    context = {
        'books': bookmarked_books,  # Use 'books' as in homepage for consistency
    }
    return render(request, 'core/bookmarked_books.html', context)

@login_required
def view_finalized_books(request):
    # Get finalized books for the logged-in user
    finalized_books = FinalizedBook.objects.filter(user=request.user)

    # Prepare data to send back as JSON
    finalized_books_list = [{
        "title": book.book.title,
        "borrow_date": book.borrow_date.strftime('%Y-%m-%d'),
        "return_date": book.return_date.strftime('%Y-%m-%d')
    } for book in finalized_books]

    return JsonResponse({"finalized_books": finalized_books_list})

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import FinalizedBook

logger = logging.getLogger(__name__)

@login_required
def return_finalized_book(request, asin):
    logger.info(f"Attempting to return finalized book with ASIN: {asin}")
    if request.method == 'POST':
        finalized_book = get_object_or_404(FinalizedBook, book__asin=asin, user=request.user)
        finalized_book.delete()
        return JsonResponse({'status': 'success', 'message': 'Book returned successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
@csrf_exempt  # You might want to secure this later
def return_borrowed_book(request, asin):
    if request.method == 'POST':
        try:
            # Fetch the borrowed book record
            borrowed_book = BorrowedBook.objects.get(book__asin=asin, user=request.user)

            # Check if the book has already been returned
            if borrowed_book.return_date is not None:
                return JsonResponse({'status': 'error', 'message': 'Book has already been returned.'})

            # Update the return date to now
            borrowed_book.return_date = timezone.now()
            borrowed_book.save()

            return JsonResponse({'status': 'success'})
        except BorrowedBook.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Book not found or not borrowed by you.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def add_to_cart(request, asin):
    book = get_object_or_404(Book, asin=asin)
    
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if book in cart.books.all():
        messages.info(request, f"'{book.title}' is already in your cart.")
    else:
        cart.books.add(book)
        messages.success(request, f"You added '{book.title}' to your cart.")
    
    return redirect('homepage')  # Redirect to homepage or cart page


@login_required
def remove_from_cart(request, asin):
    if request.method == "POST":
        cart = get_object_or_404(Cart, user=request.user)
        book = get_object_or_404(Book, asin=asin)
        
        if book in cart.books.all():
            cart.books.remove(book)
            messages.success(request, f"'{book.title}' has been removed from your cart.")
        else:
            messages.info(request, f"'{book.title}' was not found in your cart.")
        
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'books': cart.books.all(),
    }
    return render(request, 'core/view_cart.html', context)  # Create a template for viewing the cart



