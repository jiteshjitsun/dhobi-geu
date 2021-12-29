from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home/home.html')

def signin(request):
    return render(request, 'home/login.html')

def signup(request):
    return render(request, 'home/signup.html')

def contactForm(request):
    return render(request, 'home/contactForm.html')