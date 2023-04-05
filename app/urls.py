from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns=[
    path('estoque/', ProductList.as_view(), name= 'products'),
    path('estoque/<int:pk>/', ProductDetail.as_view(), name='product')
]

