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
        if not self.pk:
            existing_product = Product.objects.filter(user=self.user, name=self.name).first()
            if existing_product:
                existing_product.quantity = self.quantity
                existing_product.price = self.price
                existing_product.save()
                return existing_product
        return super().save(*args, **kwargs)
    