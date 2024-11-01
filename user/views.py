from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import UserRegistrationForm

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['usr_name']
            password = form.cleaned_data['usr_pass']
            roll_number = form.cleaned_data['usr_roll']
            dob = form.cleaned_data['usr_dob']
            email = form.cleaned_data['usr_email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Check if the username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('user:register')

            # Create the new user
            user = CustomUser(
                username=username,
                email=email,
                roll_number=roll_number,
                date_of_birth=dob,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)  # Use set_password to hash the password
            user.save()  # Save the user to the database

            messages.success(request, 'Account created successfully')
            return redirect('user:user_login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()  # Create an empty form

    return render(request, 'core/register.html', {'form': form})

# User login view
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

# User portal view
def user_portal(request):
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to homepage if user is authenticated
    else:
        messages.error(request, "You need to log in to access this page.")
        return redirect('user_login')  # Redirect to login if not authenticated
