from django.urls import path
from .views import ProductCreate, ProductList, ProductDetail, Home, Login
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('estoque/', ProductList.as_view(), name= 'products'),
    path('estoque/<int:pk>/', ProductDetail.as_view(), name='product'),
    path('estoque/cadastro/', ProductCreate.as_view(), name='product-create'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout')
]
