import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from apps.product.forms import ProductForm, ProductSearchForm
from apps.product.models import Category, Designation, Product, Size
from django.urls import reverse

# Create your views here.
def products(request):
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

    products_string = ''
    for product in Product.objects.all():
        editurl = reverse('edit_product', args=[product.slug])
        detailurl = reverse('detail_product', args=[product.slug])
        p = "{'id': '%s', 'slug': '%s', 'code': '%s', 'designation': '%s', 'description': '%s', 'size': '%s', 'category': '%s', 'editurl': '%s', 'detailurl': '%s',}," % \
            (product.id, product.slug, product.code, product.designation.labelle, product.designation.description, product.size.labelle, product.category.labelle, editurl, detailurl)

        products_string = products_string + p
    context = {
        'products_string': products_string,
        'form_s': ProductSearchForm()
    }
    
    return render(request, 'product/list.html', context)


@login_required()
def add_product(request):
    if request.method == 'POST':

        p = Product.objects.filter(category=request.POST['category'], designation=request.POST['designation'], size=request.POST['size'])
        if p:
            messages.warning(request, 'Un autre produit est enregistré avec ces informations !')
            return redirect('add_product')

        print(request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            if int(product.id) < 10:
                product.code = product.designation.labelle.capitalize()+'_0000'+str(product.id)+'P'
            elif int(product.id) < 100:
                product.code = product.designation.labelle.capitalize() + '_000' + str(product.id) + 'P'
            elif int(product.id) < 1000:
                product.code = product.designation.labelle.capitalize() + '_00' + str(product.id) + 'P'
            elif int(product.id) < 10000:
                product.code = product.designation.labelle.capitalize() + '_0' + str(product.id) + 'P'
            else :
                product.code = product.designation.labelle.capitalize() + '_' + str(product.id) + 'P'
            product.save()

            messages.success(request, 'The product has been saved successfully !')

            return redirect('products')

    else:
        form = ProductForm()
        context={
            'form': form
        }
    return render(request, 'product/add.html', context)


@login_required()
def edit_product(request, slug):
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            messages.info(request, "This changes has been saved successfully !")

            return redirect('products')
        else:
            messages.warning(request, 'The form is not valid. Please give valid information.')
            return redirect('edit_product')
    else:
        form = ProductForm(instance=product)
        context={
            'product': product,
            'form': form
        }
    
    return render(request, 'product/edit.html', context)


def detail_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    colors = product.color.all()
    context = {
        'product': product,
        'colors': colors
    }

    return render(request, 'product/detail.html', context)


def categories(request):
    context={
        'categories': Category.objects.all()
    }
    
    return render(request, 'category/list.html', context)


class CreateCategory(View):
    print('Create')
    def get(self, request):
        labelle1 = request.GET.get('labelle', None)
        description1 = request.GET.get('description', None)

        print(labelle1)
        obj = Category.objects.create(
            labelle=labelle1,
            description=description1,
        )

        category = {'id': obj.id, 'labelle': obj.labelle, 'description': obj.description, }

        data = {
            'category': category
        }
        return JsonResponse(data)


class UpdateCategory(View):
    print('Update')
    def get(self, request):
        id1 = request.GET.get('id', None)
        labelle1 = request.GET.get('labelle', None)
        description1 = request.GET.get('description', None)
        print(labelle1)
        obj = Category.objects.get(id=id1)
        obj.labelle = labelle1
        obj.description = description1
        obj.save()

        category = {'id': obj.id, 'name': obj.labelle, 'description': obj.description}

        data = {
            'category': category
        }
        return JsonResponse(data)


class DeleteCategory(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Category.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


def sizes(request):
    context={
        'sizes': Size.objects.all()
    }
    
    return render(request, 'size/list.html', context)


class CreateSize(View):
    def get(self, request):
        labelle1 = request.GET.get('labelle', None)
        description1 = request.GET.get('description', None)

        obj = Size.objects.create(
            labelle=labelle1,
            description=description1,
        )

        size = {'id': obj.id, 'labelle': obj.labelle, 'description': obj.description, }

        data = {
            'size': size
        }
        return JsonResponse(data)


class UpdateSize(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        labelle1 = request.GET.get('labelle', None)
        description1 = request.GET.get('description', None)
        obj = Size.objects.get(id=id1)
        obj.labelle = labelle1
        obj.description = description1
        obj.save()

        size = {'id': obj.id, 'name': obj.labelle, 'description': obj.description}

        data = {
            'size': size
        }
        return JsonResponse(data)


class DeleteSize(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Size.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


def designations(request):
    context={
        'designations': Designation.objects.all()
    }
    
    return render(request, 'designation/list.html', context)


class CreateDesignation(View):
    def get(self, request):
        labelle1 = request.GET.get('labelle', None)
        description1 = request.GET.get('description', None)

        obj = Designation.objects.create(
            labelle=labelle1,
            description=description1,
        )

        designation = {'id': obj.id, 'labelle': obj.labelle, 'description': obj.description, }

        data = {
            'designation': designation
        }
        return JsonResponse(data)


class UpdateDesignation(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        labelle1 = request.GET.get('labelle', None)
        description1 = request.GET.get('description', None)
        obj = Designation.objects.get(id=id1)
        obj.labelle = labelle1
        obj.description = description1
        obj.save()

        designation = {'id': obj.id, 'name': obj.labelle, 'description': obj.description}

        data = {
            'designation': designation
        }
        return JsonResponse(data)


class DeleteDesignation(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Designation.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)