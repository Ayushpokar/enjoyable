from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User, Group, Permission, ContentType
from .forms import *
import json
from .models import *
from rest_framework import serializers
from  rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

#from django.db import IntegrityError


def index(request):
    # return HttpResponse('hello')
    return render(request, 'index.html', {'title': 'Home'})


def about(request):
    return HttpResponse('this is about page and store all information about project.')


def contact(request):
    return HttpResponse('this is for contact information of our admin. ')


def schedules(request):
    return HttpResponse('this page is for train schedules.')


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


# addd trains in database

def addtrains(request): 
     if  request.method == 'POST' :
            form =AddTrainForm(data=request.POST)
            if form.is_valid():
               train_no= form.cleaned_data['train_no']
               train_name = form.cleaned_data['train_name']
               source_station = form.cleaned_data['source_station']
               dest_station = form.cleaned_data['dest_station']
               depart_datetime= form.cleaned_data['depart_datetime']
               arrival_datetime= form.cleaned_data['arrival_datetime']
               journey_duration= form.cleaned_data['journey_duration']
               available_seats =  int(form.cleaned_data['available_seats'])
               total_seats=int(form.cleaned_data('total_seats'))
               new_train = train_master('train_no','train_name', 'source_station', 'dest_station','depart_datetime','arrival_datetime','journey_duration',
                                        'total_seats')
               new_train.save()
            else:
                 return  HttpResponse("Invalid Form Data")
     else:
          form = AddTrainForm()
     return render(request,'addtrains.html',{'form':AddTrainForm})

# for add stations

def addstation(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('successfully added station.')  # Replace 'success_page' with the URL to redirect after successful form submission
    else:
        form = StationForm()

    return render(request, 'station.html', {'form': StationForm})


# def addfriend(request):
#     friend = Friend()
#     friend.user1 = request.user
#     friend.user2 = User.objects.get(id=int(request.GET['add']))
#     friend.status = "Pending"
#     friend.save()

'''@api_view(['POST','GET'])
def passenger_views(request,format=None):
    if request.method == 'POST': #for creating a new passenger
        serializer = PassMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
    elif request.method=='GET':   #for getting all passengers or details of a particular passenger
        if 'pk' in request.query_params:
            pk = int(request.query_params['pk'][0])
            try:
                passenger = passenger_master.objects.get(pass_id=pk)
                serializer = PassMasterSerializer(passenger)
                return Response(serializer.data)
            except passenger_master.DoesNotExist:
                return HttpResponse(status=404)
        else:
            passengers = passenger_master.objects.all()
            serializer = PassMasterSerializer(passengers,many=True)
            return Response(serializer.data)
'''            
'''
@csrf_exempt
@api_view(['PUT','PATCH'])
def update_passenger(request,pk):
    try:
        passenger = passenger_master.objects.get(pass_id=pk)
    except passenger_master.DoesNotExist:
        return HttpResponse(status=404)
        
    if request.method == 'PATCH':  #partial update
        serializer = PassMasterSerializer(passenger,data=request.data, partial=True)
    else:                           #full update
        serializer = PassMasterSerializer(passenger,data=request.data)
        
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)    

#this function is used to delete the record from database
@api_view(['DELETE'])
def delete_passenger(request,pk):
    try:
        passenger = passenger_master.objects.get(pass_id=pk)
        passenger.delete()
        return HttpResponse(status=204)
    except passenger_master.DoesNotExist:
        return HttpResponse(status=404)    
'''
# this function is for add trains
'''
def addtrains(request): 
    context={}
    if request.POST:  
        form=trainForm(request.POST)            
        if form.is_valid():             
            trainname=form.cleaned_data['trainName']
            source=form.cleaned_data['sourceStation']
            destination=form.cleaned_data['destinationStation']
            dep_time=form.cleaned_data['departureTime']
            arr_time=form.cleaned_data['arrivalTime']
            coach_type=form.cleaned_data['coachType']
            available_seats=form.cleaned_data['availableSeats']
            t=Train([trainname,source,destination,dep_time,arr_time,coach_type])
            t.save()
            c=Coaches(t,coach_type,[i for i in range(1,available_seats+1)])
            c.save()
            return redirect('addtrains')
        else:                            
            context["error"]="Error! Please check your entries."         
    else:            
        form=AddTrainForm()     
    context["form"]=form            
    return render(request,'addtrains.html',context)        

def viewtrains(request):
    trains=Train.objects.all().order_by("-trainId")
    return render(request,"viewtrains.html",{"trains":trains})

def deletetrain(request,tid):
    try:
        t=Train.objects.get(trainId=tid)
        Train.removeTrain(t)
        return redirect('/viewtrains/') 
    except Train.DoesNotExist:              
       return HttpResponse(status=404)                              
     
#-------------------------------------------------------------------------------    
from django.shortcuts import get_object_or_404  
from .models import Booking,Train,UserProfile,PaymentDetails
import datetime
from django.http import JsonResponse
@login_required
def booknow(request):
    tid = request.GET.get('id','')
    #print(tid)
    if not tid :
        return HttpResponseRedirect("/bookings/")
    train = get_object_or_404(Train,pk=tid)
    users=UserProfile.objects.filter(user=request.user).first()
    if 'passenger' in request.POST:
        passenger=request.POST['passenger'] 
        if passengers.isdigit():
            nofpassengers=int(passengers)                       
            request.session['nofpassengers']=nofpassengers                        
            return JsonResponse({"message":"    Passengers added Successfully!"},safe=False)    
        else:   
            return JsonResponse({"errormsg":"Invalid number of Passengers"},safe=False)                            
    elif "submit" in request.POST:                           
        try:
            nofpassengers=request.session['nofpassengers']             
            b=Booking(user=users,train=train,numberOfPassengers =nofpassengers,dateTime=datetime.datetime.strptime(request.POST['
            b=Booking(user=users,train=train,numberOfPassengers=nofpassengers,dateOfJourney=datetime.datetime.strptime(request


'''
       

    
