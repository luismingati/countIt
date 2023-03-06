from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Product

from django.shortcuts import render, get_object_or_404

def vender_produto(request, pk):
    produto = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        quantidade_vendida = int(request.POST.get('quantidade_vendida'))
        try:
            produto.atualizar_estoque(quantidade_vendida)
        except ValueError as error:
            return render(request, 'app/erro.html', {'error_message': str(error)})
        return render(request, 'app/venda_concluida.html', {'produto': produto, 'quantidade_vendida': quantidade_vendida})
    return render(request, 'app/vender_produto.html', {'produto': produto})

class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('products')

class RegisterPage(FormView):
    template_name = 'app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('products')
        return super(RegisterPage, self).get(*args, **kwargs)

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context['products'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['products'] = context['products'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'app/product.html'

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['title', 'description', 'quantity', 'price']
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProductCreate, self).form_valid(form)

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products')
    
class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('products')