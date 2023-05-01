from django.shortcuts import redirect
from .models import Product, Cart, CartItem
from .forms import ProductForm
import json
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect('products')
        
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
                if not hasattr(user, 'cart'):
                    Cart.objects.create(user=user)
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
            Cart.objects.create(user=user) 
            login(request, user)
            return redirect('products')
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def product_list(request):
    products = Product.objects.filter(user=request.user)
    context = {'products': products}
    
    search_input = request.GET.get('search-area') or ''
    if search_input:
        context['products'] = context['products'].filter(name__icontains=search_input)
    return render(request, 'app/product_list.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    context = {'product': product}
    return render(request, 'app/product_detail.html', context)

@login_required
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
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
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

@login_required
def cart_view(request):
    products = Product.objects.filter(user=request.user).order_by('-quantity')
    context = {'products': products}
    return render(request, 'app/cart.html', context)

@login_required
def complete_sale(request):
    if request.method == 'POST':
        cart_items_json = request.POST.get('cart_items')
        cart_items_data = json.loads(cart_items_json)

        for product_id, item_data in cart_items_data.items():
            product = get_object_or_404(Product, pk=product_id, user=request.user)
            quantity = int(item_data['quantity'])

            if product.quantity < quantity:
                return redirect('cart')

            product.quantity -= quantity
            product.save()

        return redirect('cart')

