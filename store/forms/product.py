from django import forms
from store.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'bar_code',
            'name',
            'category',
            'supplier',
            'cost',
            'price',
            'quantity',
            'on_display',
            'with_serial',
            'image'
        ]
        # widgets = {
        #     'bar_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bar code'}),
        #     'name': forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Name'}),
        #     'cost': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Cost'}),
        #     'price': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Price'}),
        #     'quantity': forms.NumberInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Quantity'}),
        #     'category': forms.Select(attrs={'class': 'form-control mb-2', 'placeholder': 'Category'}),
        #     'supplier': forms.Select(attrs={'class': 'form-control mb-2', 'placeholder': 'Supplier'}),
        #     'image': forms.FileInput(attrs={'class': 'form-control mb-2'}),
        #     'with_serial': forms.CheckboxInput(attrs={'class': 'form-check-input mb-2'}),
        #     'on_display': forms.CheckboxInput(attrs={'class': 'form-check-input mb-2'}),
        # }