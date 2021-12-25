from typing import Type
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from dhobiGeu import settings
from dhobiGeu.info import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage,send_mail

def home(request) : 
    return render(request,'auth/index.html')
    # return HttpResponse("hare ram")

def signup(request) : 
    if request.method == "POST" :
        # username = request.POST.get("username")
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username) :
            messages.error(request,"username already exist try some other username ")
            return redirect('home')
        
        if User.objects.filter(email=email) :
            messages.error(request,"email already registered ")
            return redirect('home')

        if len(username) > 10 :
            messages.error(request,"username must be under 10 characters ")

        if pass1 != pass2 :
            messages.error(request,"Passwords didn't match ")

        if not username.isalnum() :
            messages.error(request,"Username must be alpha numeric ")
            return redirect('home')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"your account is successfully created, we have also sent you confirmation email please confirm your email in order to activate your account ")

        #welcome email 
        subject = "Welcome Dhobi geu"
        message = "Hare krishna " + myuser.first_name + "Thank you for visiting our website \n we have also sent confirmation email please confirm your email address in order to confirm your account \n\n thanking your jitesh sourav "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        #confirmation email
        current_site = get_current_site(request)
        email_subject = "confirm your email @dobhi geu - django login!"
        message2 = render_to_string('email_confirmation.html',{
            'name' : myuser.first_name,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token' : generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True



        return redirect('signin')

    return render(request,"auth/signup.html")


def signin(request) : 

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username,password=pass1)

        if user is not None :
            login(request,user)
            fname = user.first_name
            return render(request,"auth/index.html",{'fname':fname})
        else :
            messages.error(request,"Bad Credentials!")
            return redirect('home')

    return render(request,"auth/signin.html")


def signout(request) : 
    logout(request)
    messages.success(request,"Logged out Successfully ")
    return redirect('home')

def activate(request,uid64,token) :
    try : 
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist) :
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser,token) : 
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else : 
        return render(request,'activation_failed.html')
    