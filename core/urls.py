from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views
from core.views import CustomLogoutView

urlpatterns = [
    #path('', views.index, name='index'),  # Home page (index)
    path('', views.homepage, name='homepage'),  # Homepage displaying books and search functionality
    path('index/', views.index, name='index'),  # Redirects to the main index (login page)
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin login page
    #path('user-login/', views.user_login, name='user_login'), #kept in user/urls
    path('admin-portal/', views.admin_portal, name='admin_portal'),  # Admin portal page
    #path('user-portal/', views.user_portal, name='user_portal'),  # User portal page keot in user/urls
    path('add-book/', views.add_book, name='add_book'),  # Add book page
    path('buy-book/', views.buy_book, name='buy_book'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Keep only your custom logout view
    #path('register/', views.register, name='register'), #kept in user/urls
    
]

handler404 = 'core.views.error_404'


