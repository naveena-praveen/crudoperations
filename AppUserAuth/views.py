from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.decorators.cache import cache_control
import re 
from django.core.cache import cache


# clear all cashe
def clear_all_cache():
    cache.clear()

# Cache control for the home view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request): 
    clear_all_cache()
    return render(request, 'home.html') 

# Cache control for the login view
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('home') 
        else:
            # Auth fails
            messages.error(request, 'Invalid username or password.')
            return redirect('login')   
    
    if request.method == 'GET': 
        if request.user.is_authenticated:
            return redirect('home') 
        
        return render(request, 'login.html')
    
# Cache control for the register view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    
    if request.method == 'GET': 
        if request.user.is_authenticated:
            return redirect('home') 
    
    if request.method == 'POST':
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        username = request.POST['username'].strip()
        password1 = request.POST['password1'].strip()
        password2 = request.POST['password2'].strip()
        email = request.POST['email'].strip()
        
        # List for values 
        values = [first_name, last_name, username, password1, password2, email]
             
        # Check for empty spaces
        for i in values:
            if not i:
                messages.error(request,   f'oops!! value  missing')
                return render(request, 'register.html') 
        
        # space validation for first_name 
        if not first_name:
            messages.error(request, 'Please Ensure that First Name  not been be empty or contain only spaces.') 
            return render(request, 'register.html') 
        
        # space validation for first_name 
        if not last_name:
            messages.error(request, 'Please Ensure that Last Name  not been be empty or contain only spaces.') 
            return render(request, 'register.html')
      
        # Username filter
        if not re.match(r'^\w+$', username):
            messages.error(request, 'Username can only contain letters, numbers, and underscores.')
            print('Username contains invalid characters')
            return render(request, 'register.html') 
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            print('Username already exists')
            messages.error(request, "Username already exists.")
            return render(request, 'register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            print('Email already exists')
            messages.error(request, "Email already exists.")
            return render(request, 'register.html')
        
        # email validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return render(request, 'register.html', {'values': request.POST})

        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html') 
        
        # Check password length
        if len(password1) < 8:
            print('Password is too short')
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'register.html')
        
        # Create the user
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'User created, now you can log in.')
        return redirect('login') 
    else:      
        return render(request, 'register.html')

# Cache control for the logout view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    clear_all_cache() 
    messages.success(request, 'You have been logged out.')
    return redirect('home') 


