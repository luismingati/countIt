from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Product

class Home(TemplateView):
    template_name = 'app/index.html'
    context_object_name = 'home'

class Login(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('products')
    
class Register(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('products')
        return super(Register, self).get(*args, **kwargs)

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context['products'].filter(user = self.request.user)
        return context

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'quantity', 'price']
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductCreate, self).form_valid(form)


class ProductUpdate(UpdateView):
    model = Product
    fields = ['name', 'quantity', 'price']
    success_url = reverse_lazy('products')
