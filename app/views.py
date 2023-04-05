from django.shortcuts import render

def productList(request):
    return render(request, 'index.html')

