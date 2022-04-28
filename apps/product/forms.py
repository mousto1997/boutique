from django.forms import ModelForm
from django import forms

from apps.product.models import Category, Designation, Product


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['labelle'].widget.attrs['class'] = 'input'
        self.fields['labelle'].widget.attrs['v-model'] = 'labelle'
        self.fields['description'].widget.attrs['class'] = 'textarea'


class DesignationForm(ModelForm):
    class Meta:
        model = Designation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)
        self.fields['labelle'].widget.attrs['class'] = 'input'
        self.fields['labelle'].widget.attrs['v-model'] = 'labelle'
        self.fields['description'].widget.attrs['class'] = 'textarea'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['slug', 'created_by']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['code'].widget.attrs['v-model'] = 'code'
        self.fields['category'].widget.attrs['class'] = 'input'
        self.fields['designation'].widget.attrs['class'] = 'input'
        self.fields['size'].widget.attrs['class'] = 'input'
        self.fields['price'].widget.attrs['class'] = 'input'


class ProductSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    name = forms.CharField(required=False)
    class Meta:
        model = Product
        fields = ['category', 'code', 'designation', 'size']

    def __init__(self, *args, **kwargs):
        super(ProductSearchForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['designation'].widget.attrs['class'] = 'form-control'
        self.fields['size'].widget.attrs['class'] = 'form-control'
