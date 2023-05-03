from django.shortcuts import redirect
from .models import Product, Cart
from .forms import ProductForm
from django.http import JsonResponse
from json import JSONDecodeError
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
    show_low_stock = request.GET.get('show_low_stock') == 'true'

    products = Product.objects.filter(user=request.user)
    context = {'products': products}
    
    search_input = request.GET.get('search-area') or ''
    if search_input:
        context['products'] = context['products'].filter(name__icontains=search_input)

    if show_low_stock:
        low_stock_products = []
        for product in products:
            if product.quantity <= product.min_quantity:
                low_stock_products.append(product)
        products = low_stock_products
        context = {'products': products}

   
    if show_low_stock and search_input:
        low_stock_products = []
        for product in products:
            if product.quantity <= product.min_quantity:
                low_stock_products.append(product)
        products = low_stock_products
        context = {'products': products}

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

    search_input = request.GET.get('search-area') or ''
    if search_input:
        context['products'] = context['products'].filter(name__icontains=search_input)
        
    return render(request, 'app/cart.html', context)

@login_required
def complete_sale(request):
    if request.method == 'POST':
        cart_items_json = request.POST.get('cart_items')
        
        # Verifique se cart_items_json não está vazio
        if not cart_items_json:
            return redirect('cart')
        
        try:
            cart_items_data = json.loads(cart_items_json)
        except JSONDecodeError:
            return redirect('cart')

        sale_items = []
        total_sale = 0

        if not cart_items_data:
            return redirect('cart')

        for product_id, item_data in cart_items_data.items():
            product = get_object_or_404(Product, pk=product_id, user=request.user)
            quantity = int(item_data['quantity'])
            if product.quantity < quantity:
                return redirect('cart')
            product.quantity -= quantity
            product.save()

            total_item = product.price * quantity
            sale_item = {
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': total_item
            }
            sale_items.append(sale_item)
            total_sale += total_item

        context = {'sale_items': sale_items, 'total_sale': total_sale}
        return render(request, 'app/sale_completed.html', context)

    return redirect('cart')

@login_required
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(user=request.user, name__icontains=query).order_by('-quantity')
    product_data = [{'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity} for product in products]
    return JsonResponse({'products': product_data})