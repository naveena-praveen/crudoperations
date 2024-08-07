from django.db import models

# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    username=models.CharField(max_length=150,unique=True)
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)
    
    def __str__(self):
        return self.username
    