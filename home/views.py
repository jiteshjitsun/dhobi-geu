from django.shortcuts import render
from .models import Product
# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request,'home/home.html',context)

def signin(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')

def contactForm(request):
    return render(request, 'home/contactForm.html')

def userprofile(request):
    return render(request, 'home/userprofile.html')