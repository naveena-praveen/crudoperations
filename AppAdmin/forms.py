from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm


# update user
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email'] 
        
        
# add user
class UserCreationFormExtended(UserCreationForm):
    first_name = forms.CharField(required=True) 
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    
    class meta:
        model = User 
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
    