from django.urls import path
from .views import ProductCreate, ProductList, ProductDetail, Home, Login, Register, ProductUpdate
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('', Home.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('estoque/', ProductList.as_view(), name= 'products'),
    path('estoque/<int:pk>/', ProductDetail.as_view(), name='product'),
    path('estoque/cadastro/', ProductCreate.as_view(), name='product-create'),
    path('estoque/editar/<int:pk>/', ProductUpdate.as_view(), name='product-update'),
]
