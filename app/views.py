from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Product

def productList(request):
    return render(request, 'index.html')

class ProductCreate(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')