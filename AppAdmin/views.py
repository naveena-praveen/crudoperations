
from django.shortcuts import render , redirect , get_object_or_404
from AppAdmin.forms import UserCreationFormExtended, UserUpdateForm
from AppUserAuth.views import * 
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required



# cache 
def clear_all_cache():
    cache.clear()

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request): 
    clear_all_cache()
    return render(request, 'adminlogin.html') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_panel(request): 
    if request.user.is_authenticated:
         clear_all_cache()
         return render(request, 'index.html') 
    else:
        return  redirect('admin_panel')  


# admin login 
@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate user
        user = auth.authenticate(username=username, password=password) 
        
        if user is not None:
            if user.is_superuser:  # Check if the user is a superuser
                auth.login(request, user)
                clear_all_cache()
                messages.success(request, f'{username}  logged in.')
                return redirect('admin_panel') 
            else:
                messages.error(request, 'You do not have admin privileges.')
                return redirect('admin_login')
        else:
            # Auth fails
            messages.error(request, 'You do not have admin privileges.')
            clear_all_cache()
            return redirect('admin_login')
        
    if request.method == 'GET': 
        if request.user.is_authenticated:
            return redirect('admin_panel') 
        
        # checking if user is admin by using super user
        # admin name: alan
        # admin password : 1234 
    # validation
    if request.method == 'GET': 
        if request.user.is_authenticated:
            # Check if the user is a superuser
            if request.user.is_superuser:  
                return redirect('admin_panel')
            else:
                # if user is not admin
                messages.error(request, 'You do not have admin privileges.')
                auth.logout(request)
                return redirect('admin_login')

        return render(request, 'adminlogin.html')
    
# display users 
def user_display(request):
        if request.user.is_authenticated and request.user.is_superuser:
            # Retrieve all users from the database
            users = User.objects.all().order_by('id')
            user_count = users.count() 
            return render(request, 'index.html', {'users': users , 'user_count' : user_count})
        else:
            return redirect('admin_login')  
        
         
        
        
# logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    auth.logout(request) 
    messages.success(request, 'You have been logged out.')
    clear_all_cache()
    return redirect('admin_home') 


# to delete the user
def delete_user(request,user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        user_to_delete = get_object_or_404(User, id=user_id)
        if user_to_delete != request.user:
            user_to_delete.delete()
            clear_all_cache()
            messages.success(request, 'User has been deleted successfully.')
        else:
            messages.error(request, 'You cannot delete yourself.')
    else:
        messages.error(request, 'You do not have permission to delete users.') 
    return redirect('admin_panel') 


# user update model 
@login_required
def user_update(request,user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = get_object_or_404(User , id= user_id) 
        
        if request.method == 'POST':
            form = UserUpdateForm(request.POST,instance=user)
            if form.is_valid():
                form.save() 
                clear_all_cache()
                return redirect('admin_panel')
            
        else: 
            form = UserUpdateForm(instance=user) 
        return render(request,'user_update.html', {'form': form, 'user': user})
    else:
         return redirect('admin_panel') 
     
     
# add user 
@login_required
def add_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = UserCreationFormExtended(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_panel')
        else:
            form = UserCreationFormExtended()
        
        return render(request, 'add_user.html', {'form': form})
    else:
        return redirect('admin_panel')

        
       




