from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def home(request):
    #return HttpResponse('hello i am creating account.')
    return render(request,'index1.html')

def login(request):
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        firstname= request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        password =request.POST['password']
        dob=request.POST['dob']
        email = request.POST['email']
        mobile=request.POST['mobile']
        address=request.POST['address']
        
        myuser =User.objects.create_user(username=username,email=email,password=password)
        

        myuser.save()

        messages.success(request,'your account has been successfully created.')
        return redirect('login')
    return render(request,'register.html')

