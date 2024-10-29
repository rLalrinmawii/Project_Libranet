from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        # Create an instance of the form and populate it with data from the request
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            # Get the cleaned data from the form
            username = form.cleaned_data['usr_name']
            password = form.cleaned_data['usr_pass']
            roll_number = form.cleaned_data['usr_roll']
            dob = form.cleaned_data['usr_dob']
            email = form.cleaned_data['usr_email']

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
            )
            user.set_password(password)  # Use set_password to hash the password
            user.save()  # Save the user to the database

            # Set a success message
            messages.success(request, 'Account created successfully')
            return redirect('user:user_login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()  # Create an empty form

    return render(request, 'core/register.html', {'form': form})  # Render the form


@login_required  # Ensure only logged-in users can access the user portal
def user_portal(request):
    return render(request, 'core/user_portal.html')  # Adjust template path as needed




def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('index')  # Redirect to homepage or dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('user:user_login')  # Redirect back to login page on failure

    return render(request, 'core/usr_login.html')
