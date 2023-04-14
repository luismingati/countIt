from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0.1)])
    
    def __str__(self): 
        return self.name

    def save(self, *args, **kwargs):
        # Check if the instance being saved is an existing product
        if self.pk:
            return super().save(*args, **kwargs)
        
        # If it's a new product, check if a product with the same name and user exists
        existing_product = Product.objects.filter(user=self.user, name=self.name).first()
        if existing_product:
            # If a product with the same name and user exists, update that product instead of creating a new one
            existing_product.quantity = self.quantity
            existing_product.price = self.price
            existing_product.save()
            return existing_product
        
        # If no product with the same name and user exists, save the new product
        return super().save(*args, **kwargs)
    