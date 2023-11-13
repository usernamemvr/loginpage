from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from login import settings
from django.core.mail import send_mail 
 
# Create your views here.

def home(request):
    return render(request,"authentication/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username =username):
            messages.error(request,"Username already used :(")
            return redirect('home')
        
        if User.objects.filter(email =email):
            messages.error(request,"Email already used :(")
            return redirect('home')

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        my_user = User.objects.create_user(username,email,pass1)
        my_user.first_name = fname
        my_user.last_name = lname

        my_user.save()

        messages.success(request,"Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        # Welcome Email  
        subject = "Welcome to ***** **** !!"
        message = "Hello " + my_user.first_name + "!! \n" + "Welcome to ***** ****!! \nThank you for visiting our website \nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Mr Durden"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)
        if user is not None:
            login(request,user) 
            fname = user.first_name
            return render(request,"authentication/index.html",{'fname':fname})
        else:
            messages.error(request, "Bad credentials!")
            return redirect("home")
        
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')