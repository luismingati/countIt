from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True, unique=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    productId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self): 
        return self.name

    