from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from .views import simple_logout  # Importing only the simple logout

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Homepage displaying books and search functionality
    path('index/', views.index, name='index'),  # Redirects to the main index (login page)
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin login page
    path('user-login/', views.user_login, name='user_login'),  # User login page
    path('admin-portal/', views.admin_portal, name='admin_portal'),  # Admin portal page
    path('user-portal/', views.user_portal, name='user_portal'),  # User portal page
    path('add-book/', views.add_book, name='add_book'),  # Add book page
    path('buy-book/', views.buy_book, name='buy_book'),
    path('logout/', simple_logout, name='logout'),  # Keep only the simple logout view
    path('list_users/', views.list_users, name='list_users'),
    path('list_books/', views.list_books, name='list_books'),
]

handler404 = 'core.views.error_404'
