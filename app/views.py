from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product

class ProductList(ListView):
    model = Product

