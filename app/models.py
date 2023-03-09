from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  title =models.CharField(max_length=100)
  description = models.TextField(null=True, blank=True)
  sold = models.BooleanField(default=False)
  quantity = models.IntegerField(default=1)
  price = models.DecimalField(max_digits=6, decimal_places=2)


  def atualizar_estoque(self, quantidade_vendida):
    if quantidade_vendida > self.quantity:
      raise ValueError('Quantidade vendida é maior do que a quantidade em estoque.')
    self.quantity -= quantidade_vendida
    self.save()

  def __str__(self):
    return self.title

  class Meta:
    ordering = ['quantity']