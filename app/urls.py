from django.urls import path
from .views import product_list, product_detail,create_product, product_update, product_delete, home, login_view, register
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),
    path('estoque/', product_list, name= 'products'),
    path('estoque/<int:pk>/', product_detail, name='product'),
    path('estoque/cadastro/', create_product, name='product-create'),
    path('estoque/editar/<int:pk>/', product_update, name='product-update'),
    path('estoque/deletar/<int:pk>/', product_delete, name='product-delete'),
]
