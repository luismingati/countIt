from django.urls import path
from . import views
from .views import ProductCreate


urlpatterns=[
    path('', views.productList, name= 'products'),
    path('cadastro/', ProductCreate.as_view(), name='product-create'),
]

