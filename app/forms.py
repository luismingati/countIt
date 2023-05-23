from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'min_quantity', 'category']

    def save(self, commit=True, user=None):
        product = super().save(commit=False)
        product.user = user
        if commit:
            product.save()
        return product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
