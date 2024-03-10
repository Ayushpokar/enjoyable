import queue
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.forms import DateTimeField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User         
from .forms import *
import json
from .models import *
from datetime import datetime

#from django.db import IntegrityError


def index(request):
    # return HttpResponse('hello')
    stn =station_master.objects.all()
    return render(request, 'index.html', {'title': 'Home', 'stn': stn})

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


       return  redirect('/login')



    return render(request, 'register.html')



def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = user_master.objects.get(username=username, password=password)
            request.session['userid'] = user.id
            request.session['username'] = user.username
            user_name={
                'User':user.username
            }
            print('User Logged In Successfully!')
            return render(request,'dashboard.html',user_name)
            

        except user_master.DoesNotExist:
            messages.error(request, "User does not exist")
            return HttpResponse('Invalid Username or Password')
            
    return render(request,'login.html')


def logout_view(request):
        logout(request)
        return redirect('/login')        


# @login_required(login_url='/login')
def dashboard(request):
    print(request.user) 
    # get the current logged in user details from session and display on dashboard page
    return render(request, 'dashboard.html')

def about(request):
    return render(request,"srchtrn.html")

def contact(request):
    return HttpResponse('this is for contact information of our admin. ')


def schedules(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        duration = int(request.POST['duration'])
        try:
            obj=ScheduleMaster()
            obj.save_schedules(date,time,duration)
            messages.success(request, "Scheduled Successfully ")
            return redirect('/schedules')
        except Exception as e:
            messages.error(request, str(    e))
    else:
        schedulelist = ScheduleMaster.objects.all().order_by("-id")[:10]    
        context ={'schedulelist':schedulelist}  
        return render(request,'schedules.html',context)


def pnr_status(request):
    #return HttpResponse('this page is for check pnr status of a particular train.')
    return render(request,'pnr.html')

def cancel_ticket(request):
    #return HttpResponse("This Page Is For Canceling Tickets")
    return  render(request,"cancel.html",{'msg':'Please enter your ticket number to proceed.'})

'''@login_required()   
def post_cancel(request):
    if request.method == "POST":
        tnum = request.POST['tnum']
        uid=request.user.username
        try:
            obj = user_master.objects.get(tnumber=tnum, user=uid)
            obj.delete()
            return render(request,"cancel.html",{'msg':'Your ticket has been cancelled successfully!'})
        except Exception as e :
            print (e)
            return render(request,"cancel.html",{"error":"Error! Please Enter Correct Ticket Number."})  '''

def feedback(request):
     #return HttpResponse('this page for user give the feedback or suggestiions.')
     return render(request,'feedback.html')

'''form = FeedbackForm()
    if request.method=='POST':
       form = FeedbackForm(data=request.POST)
       if form.is_valid():  
           name = form.cleaned_data['name']
           email = form.cleaned_data['email']
           phone = form.cleaned_data['phone']
           message = form.cleaned_data['message']
           fd = feedback_details(name=name,email=email,phone=phone,feedback=message)
           fd.save()
           return render(request,'thankyou.html',{'form':form})
    else:
         return render(request,'feedback.html',{'form':form})'''

#from django.core.mail import send_mail
#def thankyou(request):
    #return render(request,'thankyou.html')
# register
        




# addd trains in database

def addtrains(request): 
     if  request.method == 'POST' :
               train_no= request.POST.get('train_no')
               train_name = request.POST.get('train_name')
               src = request.POST.get('source_station')
               dest = request.POST.get('dest_station')
               depart_time = datetime.strptime(request.POST.get('depart_time'), '%H:%M').time()
               arrival_time = datetime.strptime(request.POST.get('arrival_time'), '%H:%M').time()
               journey_duration= request.POST.get('journey_duration')
               available_seats =  int(request.POST.get('available_seats'))
               total_seats=int(request.POST.get('total_seats'))
               depart_date = datetime.strptime(request.POST.get('depart_date'), '%Y-%m-%d').date()
               arrival_date = datetime.strptime(request.POST.get('arrival_date'), '%Y-%m-%d').date()
               try:
                   source_station=station_master.objects.get(station_name=src)
                   dest_station=station_master.objects.get(station_name=dest)

               except station_master.DoesNotExist:
                   return HttpResponse("Station does not exist")
                   
               new_train = train_master(train_no=train_no,train_name=train_name, source_station=source_station, dest_station=dest_station,depart_time=depart_time,
                                        arrival_time=arrival_time,journey_duration=journey_duration,available_seats=available_seats,
                                        total_seats=total_seats,arrival_date=arrival_date,depart_date=depart_date)
               new_train.save()
               return HttpResponse('Train Added Successfully')
            
            
     else:
          HttpResponse("Something wrong. Please try again.")
     return render(request,'addtrains.html')

def addstation(request):
    if request.method == 'POST':
            station_name = request.POST['station_name']
            station_code= request.POST['station_code']
            location= request.POST['location']
            zone= request.POST['zone']
            state= request.POST['state']
            new_station=station_master(station_name=station_name,station_code=station_code,location=location,zone=zone,state=state)
            new_station.save()
            return HttpResponse('successfully added station.')  # Replace 'success_page' with the URL to redirect after successful form submission
    else:
        HttpResponse("something wrong. please try again")

    return render(request, 'station.html')
def addroutestn(request):
    if request.method=='POST':
        train_no=request.POST['train_no']
        station_id = request.POST['station_id']
        sequence_no = request.POST['sequence_no']
        arrival_time=datetime.strptime(request.POST['arrival_time'], "%H:%M").time()
        departure_time=datetime.strftime(request.POST['departure_time'],"%H:%M").time()
        print (type(arrival_time))
        route=routestation(train_no=train_no,station_id=station_id,sequence_no=sequence_no,arrival_time=arrival_time,departure_time=departure_time)
        route.save()
        
        return HttpResponse ("Route added successfully")
    else:
        return HttpResponse( "Error in adding Route")
    return render(request,"routestation.html")

# def addroutestn(request):
#     global route_stations
#     if request.method=='GET':
#          return JsonResponse([i.toJSON() for i in route_stations], safe=False)
#     elif request.method=='POST':
#        # print(route_stations)
#         stat_id=request.POST['stat_id']
#         pos=request.POST['position']
#         act=request.POST['isActive']
#         with open('static/js/routes.json','r+') as f:
#               data=json.load(f)
#               st=data[int(pos)]
#               st["isActive"]=act
#               st["staId"]=stat_id
#               data[int(pos)]=st
#               f.seek(0)
#               json.dump(data,f)
#               f.truncate()  
#               route_stations=RouteStations(route_stns=data).getRouteStns()  
#     return JsonResponse({"message":"Success"},safe=False)  

def searchtrain(request):
    # get the data from the user
    if request.method == 'POST':
        source = request.POST.get("source") 
        destination = request.POST.get("destination")
        
        
         # Query trains based on source station and destination station
        print(source,destination)
        station = {
            'src': source,
            'dest': destination
        }
        # parsed_date=None
        # if date is not None and isinstance(depart_date, str):
        #     try:
        #         parsed_date = datetime.strptime(depart_date, '%Y-%m-%d').date()
        #     except ValueError:
        #         # Handle the case when date is not in the expected format
        #         return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
        filtered_trains=[]
        filtered_trains = train_master.objects.filter(
            source_station_id=source,
            dest_station_id=destination,
        
        ).values
        print(filtered_trains,"hello")
         #       filtered_trains.append(train)

        return render(request,"searchedtrains.html",{ "trains": filtered_trains , 'station':station})
       #You can do further processing with the 'trains' queryset

            # For example, you might want to pass the results to a template
            # return render(request, 'searched_train.html', {'trains': trains})
    else:
        # If it's a GET request, create an empty form
      print("else condn chal rhi hai")

    return render(request, 'srchtrn.html' )

        
