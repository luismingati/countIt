from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)
    
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

    def save(self, commit=True, user=None):
        category = super().save(commit=False)
        category.user = user
        if commit:
            category.save()
        return category