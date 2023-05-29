from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.conf import settings
from decimal import Decimal
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'user')

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    min_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0.1)])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self): 
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            existing_product = Product.objects.filter(user=self.user, name=self.name).first()
            if existing_product:
                existing_product.quantity = self.quantity
                existing_product.min_quantity = self.min_quantity
                existing_product.price = self.price
                existing_product.save()
                return existing_product
        return super().save(*args, **kwargs)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')
    discount = models.FloatField(default=0)

    def __str__(self):
        return f'Carrinho de {self.user.username}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.FloatField(default=0)
    
    def formatted_date(self):
        return self.timestamp.strftime('%d/%m/%Y')
    
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0.1)])

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'