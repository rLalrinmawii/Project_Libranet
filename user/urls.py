from django.urls import path
from . import views

app_name = 'user' 

urlpatterns = [
    path('register/', views.register, name='register'),  # User registration URL
    path('user-login/', views.user_login, name='user_login'),  # User login page
    path('user_portal/', views.user_portal, name='user_portal'), 
]
