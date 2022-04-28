from django.contrib.auth.models import User
from django.db import models
from django.http import request
from django.urls import reverse

# Create your models here.
from django.utils.timezone import now


class Category(models.Model):
    labelle = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.labelle
    

class Designation(models.Model):
    labelle = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Designations'
        
    def __str__(self):
        return self.labelle
    
    
class Size(models.Model):
    labelle = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Sizes'
        
    def __str__(self):
        return self.labelle


class Product(models.Model):
    code = models.CharField(max_length=100)
    category = models.ForeignKey(Category, blank=True, related_name='products', on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, blank=True, related_name='products', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=True, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    price = models.FloatField()

    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.slug

