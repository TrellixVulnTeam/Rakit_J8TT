from django.shortcuts import render

def index(request):
    return render(request, 'Terms_of_Use/home.html')
