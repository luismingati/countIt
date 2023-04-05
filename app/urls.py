from django.urls import path
from .views import ProductCreate, ProductList, ProductDetail, Home
from . import views


urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('estoque/', ProductList.as_view(), name= 'products'),
    path('estoque/<int:pk>/', ProductDetail.as_view(), name='product'),
    path('estoque/cadastro/', ProductCreate.as_view(), name='product-create')
]
