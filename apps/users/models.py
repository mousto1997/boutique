from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customer(models.Model):
    phone = models.CharField(max_length=200, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='default_profile.jpg', upload_to='profile/image')
    bio = models.CharField(max_length=500, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name