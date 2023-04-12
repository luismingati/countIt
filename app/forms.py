from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price']

    name = forms.CharField(max_length=255)
    quantity = forms.IntegerField()
    price = forms.DecimalField(max_digits=6, decimal_places=2)
