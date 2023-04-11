from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product
from django.http import Http404

class Home(TemplateView):
    template_name = 'app/index.html'
    context_object_name = 'home'

class Login(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('products')

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')






