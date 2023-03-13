from django.shortcuts import render
from django.http import HttpResponse

def productList(request):
  return HttpResponse('Product List')