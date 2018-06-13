from django.shortcuts import render

def index(request):
    return render(request, 'Our_Vision/home.html')
