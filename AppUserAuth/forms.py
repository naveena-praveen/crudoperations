from django import forms 
from . models import User
class RegisterForm(forms.Form):
    first_name =forms.CharField(max_length=150, required=True)
    last_name =forms.CharField(max_length=150, required=True) 
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True) 
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True) 
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    
    
