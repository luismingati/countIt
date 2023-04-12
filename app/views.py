from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    context = {'home': True}
    return render(request, 'app/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('products')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

    
def register(request):
    if request.user.is_authenticated:
        return redirect('products')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    context = {'products': products}
    return render(request, 'app/product_list.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    context = {'product': product}
    return render(request, 'app/product_detail.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'app/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'app/product_form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    return render(request, 'app/product_delete.html', {'product': product})