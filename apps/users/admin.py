from django.contrib import admin

# Register your models here.
from apps.users.models import Customer

admin.site.register(Customer)
