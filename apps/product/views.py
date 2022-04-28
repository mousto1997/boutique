import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from apps.product.forms import ProductForm, ProductSearchForm
from apps.product.models import Category, Designation, Product, Size
from django.urls import reverse

# Create your views here.
def product_grid(request):
    products_string = ''
    for product in Product.objects.all():
        form_s = ProductSearchForm(request.POST or None)
        products = Product.objects.all()
        if request.method == 'POST':
            if form_s:
                if request.POST['category']:
                    products = Product.objects.filter(
                        category=form_s['category'].value())
                if request.POST['designation']:
                    products = Product.objects.filter(
                        designation=form_s['designation'].value())
                if request.POST['size']:
                    products = Product.objects.filter(
                        size=form_s['size'].value())

                if form_s['export_to_CSV'].value() == True:
                    response = HttpResponse(content_type='text/csv')
                    response['content-Disposition'] = 'attachment; fileName="Liste des Produts.csv"'
                    writer = csv.writer(response)
                    writer.writerow(['Category', 'Produit'])

                    for product in products:
                        writer.writerow([product.category.labelle, product.designation.labelle])
                    return response
        edit_product = reverse('product', args=[product.slug])
        p = "{'id': '%s', 'code': '%s', 'designation': '%s', 'description': '%s', 'size': '%s', 'category': '%s', 'edit': '%s',}," % \
            (product.id, product.code, product.designation.labelle, product.designation.description, product.size.labelle, product.category.labelle, edit_product)

        products_string = products_string + p
    context = {
        'products_string': products_string,
        'form_s': ProductSearchForm()

    }
    print(products_string)
    
    return render(request, 'product/list_grid.html', context)


def product_list(request):
    context={
        'products': Product.objects.all()
    }
    
    return render(request, 'product/list_list.html', context)

@login_required()
def add_product(request):
    print('Product_111111111')
    if request.method == 'POST':
        print('Product_222222222')
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()

            messages.success(request, 'The product has been saved successfully !')

            return redirect('product_list')
    else:
        form = ProductForm()
        context={
            'form': form
        }
    return render(request, 'product/add.html', context)


def product(request, slug):
    context={
        'product': get_object_or_404(Product, slug=slug)
    }
    
    return render(request, 'product/detail.html', context)


def categories(request):
    context={
        'categories': Category.objects.all()
    }
    
    return render(request, 'categorie/list.html', context)


def sizes(request):
    context={
        'sizes': Size.objects.all()
    }
    
    return render(request, 'size/list.html', context)


def designations(request):
    context={
        'designations': Designation.objects.all()
    }
    
    return render(request, 'designation/list.html', context)
