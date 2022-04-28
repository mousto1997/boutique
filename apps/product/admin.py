from django.contrib import admin

from apps.product.models import Category, Designation, Product, Size

# Register your models here.
admin.site.register(Product)
admin.site.register(Designation)
admin.site.register(Category)
admin.site.register(Size)
