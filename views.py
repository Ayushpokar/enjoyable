from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from home.models import user_master
#from django.db import IntegrityError


def index(request):
    # return HttpResponse('hello')
    return render(request, 'index.html')

def dashboard(request):
     return render(request, 'dashboard.html')

def about(request):
    return HttpResponse('this is about page and store all information about project.')


def contact(request):
    return HttpResponse('this is for contact information of our admin. ')


def schedules(request):
    return HttpResponse('this page is for train schedules.')


def pnr_status(request):
    return HttpResponse('this page is for check pnr status of a particular train.')


def cancel_ticket(request):
    return HttpResponse("This Page Is For Canceling Tickets")


def feedback(request):
     return HttpResponse('this page for user give the feedback or suggestiions.')

# register
def register(request):
    if request.method == 'POST':

       username = request.POST['username']
       password = request.POST['password']
       firstname = request.POST['firstname']
       lastname = request.POST['lastname']
       dob = request.POST['dob']
       email = request.POST['email']
       mobile = request.POST['mobile']
       address = request.POST['address']
       # for save the information of user 

       myuser = user_master.objects.create_user(firstname=firstname, lastname=lastname, username=username,
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
            return redirect('dashboard')

        except user_master.DoesNotExist:
            messages.error(request, "User does not exist")
            return HttpResponse('Invalid Username or Password')
            
    return render(request,'login.html')
         
         
    pass
    '''if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        myuser = authenticate(request, username=username, password=password)
        print(myuser)

        if myuser is not None:
            login(request, myuser)
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('/home')
        
    return render(request,'login.html')'''
        


@login_required
def dashboard(request):
        context={}
        uid = request.user.id
        usr_obj = User.objects.get(id=uid)
        context['usr'] = usr_obj

     
        print(usr_obj.email)
        print(User.objects.all())    
        user = get_object_or_404(User, id=request.user.id)
        context["user"] = user
        return render(request,"dashboard.html",context)


@login_required
def logout_view(request):
        logout(request)
        return redirect("/index")

# def addfriend(request):
#     friend = Friend()
#     friend.user1 = request.user
#     friend.user2 = User.objects.get(id=int(request.GET['add']))
#     friend.status = "Pending"
#     friend.save()


       

    
