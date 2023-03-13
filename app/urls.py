from django.urls import path
from . import views

urlpatterns = [
  path('', views.productList, name='products'),
]