from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *  # Import all models to be used in this view
import json 
from home.models import *
from home.views import *
from django.contrib.auth import  authenticate, login ,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':

       username = request.POST.get('username')
       password = request.POST.get('password')
       firstname = request.POST.get('firstname')
       lastname = request.POST.get('lastname')
       dob = request.POST.get('dob')
       email = request.POST.get('email')
       mobile = request.POST.get('mobile')
       address = request.POST.get('address')
       # for save the information of user 

       myuser = user_master(firstname=firstname, lastname=lastname, username=username,
                             password=password, dob=dob, email=email, mobile=mobile, address=address)
       myuser.save()

       
       # check user already exists or not.'''

       ''' if myuser.objects.filter(username = username).exists():
               messages.error(request, "Username already exists.")
               return redirect('/home/register')

       elif len(password) < 8:
               messages.error(request, "Password must be at least 8 characters long.")
               return redirect('/home/register')'''


       return  HttpResponse("data added successfully.")



    return render(request, 'register.html')



def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = user_master.objects.get(username=username, password=password)
            request.session['userid'] = user.id
            request.session['username'] = user.username
            print('User Logged In Successfully!')
            return redirect('home/dashboard')

        except user_master.DoesNotExist:
            messages.error(request, "User does not exist")
            return HttpResponse('Invalid Username or Password')
            
    return render(request,'login.html')
         
         

    
@login_required
def logout_view(request):
        logout(request)
        return redirect("/index")        
