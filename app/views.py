from django.shortcuts import redirect
from .models import Product, Cart, Sale, SaleItem
from .forms import ProductForm, CategoryForm
from django.http import JsonResponse
from json import JSONDecodeError
from decimal import Decimal, InvalidOperation
from datetime import datetime
from calendar import monthrange
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F
from django.db import IntegrityError
import json
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm(user=request.user)
    return render(request, 'app/product_form.html', {'form': form})
    
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product, user=request.user)
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
        discount_string = request.POST.get('discount', '').strip()

        if not cart_items_json:
            return redirect('cart')

        try:
            discount_percentage = Decimal(discount_string)
        except InvalidOperation:
            discount_percentage = Decimal('0')

        if discount_percentage < 0 or discount_percentage > 100:
            return redirect('cart')

        try:
            cart_items_data = json.loads(cart_items_json)
        except JSONDecodeError:
            return redirect('cart')

        sale_items = []
        total_sale = 0

        if not cart_items_data:
            return redirect('cart')

        sale_date = timezone.now()

        for product_id, item_data in cart_items_data.items():
            product = get_object_or_404(Product, pk=product_id, user=request.user)

            quantity = int(item_data['quantity'])
            if product.quantity < quantity:
                return redirect('cart')
            elif product.quantity <= 0:
                return redirect('cart')

            product.quantity -= quantity
            product.save()

            total_item = product.price * quantity
            total_item_discounted = total_item - (total_item * Decimal(discount_percentage) / 100)
            sale_item = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'total': total_item_discounted,
                'sale_date': sale_date
            }
            sale_items.append(sale_item)
            total_sale += total_item_discounted

        context = {
            'sale_items': sale_items,
            'total_sale': total_sale,
            'discount': discount_percentage ,
            'sale_date': sale_date
        }

        sale = Sale(user=request.user, total=total_sale)
        sale.save()

        for sale_item in sale_items:
            product = Product.objects.get(id=sale_item['id'])
            quantity = sale_item['quantity']
            total = sale_item['total']
            SaleItem(sale=sale, product=product, quantity=quantity, total=total).save()


        return render(request, 'app/sale_completed.html', context)
    return redirect('cart')

@login_required
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(user=request.user, name__icontains=query).order_by('-quantity')
    product_data = [{'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity} for product in products]
    return JsonResponse({'products': product_data})

@login_required
def create_category(request):
    error_message = ''
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save(user=request.user)
                return redirect('product-create')
            except IntegrityError:
                error_message = "Você já tem uma categoria com este nome."
                form = CategoryForm() 
    else:
        form = CategoryForm()
    return render(request, 'app/create_category.html', {'form':form, 'error_message': error_message})

@login_required
def dashboard(request):
    sales_per_month = Sale.objects.filter(user=request.user).annotate(month=TruncMonth('timestamp')).values('month').annotate(total_sales=Sum(F('total'))).order_by('-month')

    context = {
        'sales_per_month': sales_per_month,
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def monthly_sales_detail(request, year, month):
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, monthrange(year, month)[1])

    sales = Sale.objects.filter(user=request.user, timestamp__range=[first_day, last_day])

    context = {
        'sales': sales,
        'month': first_day.strftime('%B %Y'),
    }
    return render(request, 'app/monthly_sales_detail.html', context)