from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.http import request
from django.urls import reverse

# Create your models here.
from django.utils.timezone import now


class Category(models.Model):
    labelle = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.labelle
    

class Designation(models.Model):
    labelle = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Designations'
        
    def __str__(self):
        return self.labelle


class Color(models.Model):
    labelle = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)

    class Meta:
        verbose_name_plural = 'colors'

    def __str__(self):
        return self.labelle
    
    
class Size(models.Model):
    labelle = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250)
    
    class Meta:
        verbose_name_plural = 'Sizes'
        
    def __str__(self):
        return self.labelle


class Product(models.Model):
    code = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, blank=True, related_name='products', null=True, on_delete=models.SET_NULL)
    designation = models.ForeignKey(Designation, blank=True, related_name='products', null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, blank=True, related_name='products', null=True, on_delete=models.SET_NULL)
    color = models.ManyToManyField(Color, blank=True, related_name='products')
    slug = models.SlugField(max_length=250, unique=True)
    price = models.FloatField()

    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.slug


@receiver(pre_save, sender=Product)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].category.labelle+'_'+kwargs['instance'].designation.labelle+'_'+kwargs['instance'].size.labelle)
    kwargs['instance'].slug = slug

