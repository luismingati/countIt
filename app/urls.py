from django.urls import path
from . import views
from .views import ProductCreate, ProductList


urlpatterns=[
    path('estoque/', ProductList.as_view(), name= 'products'),
    path('estoque/cadastro/', ProductCreate.as_view(), name='product-create'),
]