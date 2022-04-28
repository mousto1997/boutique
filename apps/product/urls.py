from django.urls import path
from apps.product import views


urlpatterns = [
    path('liste/grid', views.product_grid, name="product_grid"),
    path('liste/liste', views.product_list, name="product_list"),
    path('<slug:slug>', views.product, name="product"),
    path('add/new', views.add_product, name="add_product"),
    
    path('categories', views.categories, name="categories"),
    path('sizes', views.sizes, name="sizes"),
    path('designations', views.designations, name="designations"),
]
