
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default='My bio')
    location = models.CharField(max_length=100, blank=True, default='My location')
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
