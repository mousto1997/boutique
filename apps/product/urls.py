from django.urls import path
from apps.product import views
from apps.product.api import api_delete_product

urlpatterns = [
    path('products', views.products, name="products"),
    path('<slug:slug>/edit', views.edit_product, name="edit_product"),
    path('<slug:slug>/detail', views.detail_product, name="detail_product"),
    path('add/new', views.add_product, name="add_product"),

    path('api/delete_product/<int:product_id>/', api_delete_product, name="api_delete_product"),

    path('categories', views.categories, name="categories"),
    path('category/create/', views.CreateCategory.as_view(), name="new_category"),
    path('category/edit/', views.UpdateCategory.as_view(), name="edit_category"),
    path('category/delete/', views.DeleteCategory.as_view(), name="delete_category"),

    path('sizes', views.sizes, name="sizes"),
    path('size/create/', views.CreateSize.as_view(), name="new_size"),
    path('size/edit/', views.UpdateSize.as_view(), name="edit_size"),
    path('size/delete/', views.DeleteSize.as_view(), name="delete_size"),

    path('designations', views.designations, name="designations"),
    path('designation/create/', views.CreateDesignation.as_view(), name="new_designation"),
    path('designation/edit/', views.UpdateDesignation.as_view(), name="edit_designation"),
    path('designation/delete/', views.DeleteDesignation.as_view(), name="delete_designation"),
]
