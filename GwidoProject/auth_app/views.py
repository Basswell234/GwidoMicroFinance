from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from village_banking.models import Person
from .forms import RegistrationForm

# Create your views here.


def register_user(request):
    """
    Handle user registration.
    Combines User model and Person model creation through signals.
    GET: Display the registration form
    POST: Process registration and create new user account
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create the User
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                
                # Update the Person profile that was automatically created by signal
                person = Person.objects.get(user=user)
                person.firstname = form.cleaned_data['first_name']
                person.lastname = form.cleaned_data['last_name']
                person.sex = form.cleaned_data['sex']
                person.address = form.cleaned_data['address']
                person.phone_number = form.cleaned_data['phone_number']
                person.email = form.cleaned_data['email']
                person.occupation = form.cleaned_data['occupation']
                person.membership_status = 'pending'
                person.membership_desc = form.cleaned_data.get('membership_desc', '')
                person.nrc = form.cleaned_data['nrc']
                person.save()
                
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
            
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")  # Redirect to login page after logout

def home(request): 
    return render(request, 'auth_app/home/home.html',{})