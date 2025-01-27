from django.urls import path
from core import views  # Core views import
from .views import simple_logout, view_finalized_books, return_finalized_book  # Import specific views only as needed
from .views import add_to_cart, remove_from_cart, view_cart

urlpatterns = [
    # Home and Index Views
    path('', views.homepage, name='homepage'),  # Homepage displaying books and search functionality
    path('index/', views.index, name='index'),  # Redirects to the main index (login page)

    # Login/Logout and User/Admin Portal Views
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin login page
    path('user-login/', views.user_login, name='user_login'),  # User login page
    path('admin-portal/', views.admin_portal, name='admin_portal'),  # Admin portal page
    path('user-portal/', views.user_portal, name='user_portal'),  # User portal page
    path('logout/', simple_logout, name='logout'),  # Simple logout view

    # Book Management Views
    path('add-book/', views.add_book, name='add_book'),  # Add book page
    path('list_users/', views.list_users, name='list_users'),  # List users page
    path('list_books/', views.list_books, name='list_books'),  # List books page

    # Bookmark Views
    path('bookmark/<str:asin>/', views.bookmark_book, name='bookmark_book'),  # Bookmark book by ASIN
    path('bookmarked-books/', views.bookmarked_books, name='bookmarked_books'),  # View bookmarked books
    path('bookmark-toggle/<int:book_id>/', views.toggle_bookmark, name='toggle_bookmark'),  # Toggle bookmark status

    # Borrowing and Returning Books
    path('borrow/<str:asin>/', views.borrow_book, name='borrow_book'),  # Borrow a book by ASIN
    path('borrowed-books/', views.borrowed_books_view, name='borrowed_books'),  # View borrowed books
    path('remove-borrowed-book/<str:asin>/', views.remove_borrowed_book, name='remove_borrowed_book'),  # Remove borrowed book
    path('finalize-borrow/', views.finalize_borrow, name='finalize_borrow'),  # Finalize borrowed books
    path('view-finalized-books/', view_finalized_books, name='view_finalized_books'),  # View finalized books

    # Return Books
    path('return-borrowed-book/<str:asin>/', views.return_borrowed_book, name='return_borrowed_book'),  # Return borrowed book
    path('return-finalized-book/<str:asin>/', return_finalized_book, name='return_finalized_book'),  # Return finalized book

    # Cart
    path('cart/add/<str:asin>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:asin>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', view_cart, name='view_cart'),

    path('chat/',views.chatbot_view, name='chatbot'),
    
    
]

# Custom Error Handler
handler404 = 'core.views.error_404'
