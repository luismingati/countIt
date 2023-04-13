from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity']

    def save(self, commit=True, user=None):
        product = super().save(commit=False)
        product.user = user
        if commit:
            product.save()
        return product
