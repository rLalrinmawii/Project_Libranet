from django.urls import path
from . import views

app_name = 'user' 

urlpatterns = [
    path('login/', views.user_login, name='user_login'),  # User login URL
    path('register/', views.register, name='register'),  # User registration URL
    path('user_portal/', views.user_portal, name='user_portal'), 
]
