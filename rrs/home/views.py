from django.db.models import Count
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import  login_required
from django.forms import DateTimeField
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.urls import reverse         
from .forms import *
import json
from django.core.serializers.json import  DjangoJSONEncoder
from .models import *
from datetime import datetime
from django.contrib.auth.hashers import make_password ,check_password
from datetime import datetime,date,timedelta




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
        hash_password = make_password(password)
        print(username,password)

        
        try:
            # passd=check_password(hash_password)
            # print(passd)
            user = user_master.objects.get(username=username, password=password)
            request.session['username'] = user.username

            # user = authenticate(username=username, password=hash_password)

            # print(user)
            # if user is not None:
            #     login(request, user)
            #     request.session['userid'] = user.id
            #     request.session['username'] = user.username
            user_name={
             'User':user.username
            }
            print('User Logged In Successfully!')
            return redirect('/dashboard')
            # else:
            #     return HttpResponse( "Invalid Login")
            

        except user_master.DoesNotExist:
            messages.error(request, "User does not exist")
            return HttpResponse('Invalid Username or Password')
            
    return render(request,'login.html')


def logout_view(request):
        logout(request)
        return redirect('/login')        


#@login_required(login_url='/login')
def dashboard(request):
    stn =station_master.objects.all()
    clss=class_master.objects.all()
    

    print(request.user)
    # Get the logged in users id from session and get all data related to that user
    user_name=request.session.get('username')
    user_name = {
        'User' : user_name
        
    }
    # get the current logged in user details from session and display on dashboard page
    return render(request, 'dashboard.html',{ 'stn': stn,'clss':clss})

def about(request):
    return render(request,"srchtrn.html")

def contact(request):
    return HttpResponse('this is for contact information of our admin. ')


def schedules(request):
    # if request.method == 'POST':
    #     date = request.POST['date']
    #     time = request.POST['time']
    #     duration = int(request.POST['duration'])
    #     try:
    #         obj=ScheduleMaster()
    #         obj.save_schedules(date,time,duration)
    #         messages.success(request, "Scheduled Successfully ")
    #         return redirect('/schedules')
    #     except Exception as e:
    #         messages.error(request, str(    e))
    # else:
    #     schedulelist = ScheduleMaster.objects.all().order_by("-id")[:10]    
    #     context ={'schedulelist':schedulelist}  
        return render(request,'trnschdle.html')


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
     if request.method =="POST":
          email= request.POST['email']
          subject= request.POST['subject']
          descrip = request.POST['descrip']
          user= user_feedback(subject=subject, message=descrip,email=email)
          user.save()

          
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
     source_stations=station_master.objects.all()
     dest_stations=station_master.objects.all()
     context= {'source_stations':source_stations , 'dest_stations':dest_stations}
     if  request.method == 'POST' :
               train_no= request.POST.get('train_no')
               train_name = request.POST.get('train_name')
               src = request.POST.get('source_station')
               dest = request.POST.get('dest_station')
               depart_time = datetime.strptime(request.POST.get('depart_time'), '%H:%M').time()
               arrival_time = datetime.strptime(request.POST.get('arrival_time'), '%H:%M').time()
               journey_duration= request.POST.get('journey_duration')
               
               try:
                   source_station=station_master.objects.get(station_code=src)
                   dest_station=station_master.objects.get(station_code=dest)

               except station_master.DoesNotExist:
                   return HttpResponse("Station does not exist")
                   
               new_train = train_master(train_no=train_no,train_name=train_name, source_station=source_station, dest_station=dest_station,depart_time=depart_time,
                                        arrival_time=arrival_time,journey_duration=journey_duration)
               new_train.save()
               return render(request,'addtrains.html')
            
            
     else:
          HttpResponse("Something wrong. Please try again.")
            
     return render(request,'addtrains.html',context)

def addstation(request):
    if request.method == 'POST':
            station_name = request.POST['station_name'].upper()
            station_code= request.POST['station_code'].upper()
            location= request.POST['location']
            zone= request.POST['zone'].upper()  
            state= request.POST['state'].upper()
            new_station=station_master(station_name=station_name,station_code=station_code,location=location,zone=zone,state=state)
            new_station.save()
            return render(request,'station.html.')  # Replace 'success_page' with the URL to redirect after successful form submission
    else:
        HttpResponse("something wrong. please try again")

    return render(request, 'station.html')
def addroutestn(request):
    stn=station_master.objects.all()
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        stations = station_master.objects.filter(station_name__icontains=query)
        results = [station.station_name for station in stations]
        return JsonResponse(results, safe=False)
    return render(request, 'routestation.html')

    # if request.method == 'POST':
    #     train_no=request.POST['train_no']
    #     station_id = request.POST['station_id']
    #     sequence_no = request.POST['sequence_no']
    #     arrival_time=datetime.strptime(request.POST['arrival_time'], "%H:%M").time()
    #     departure_time=datetime.strftime(request.POST['departure_time'],"%H:%M").time()
    #     print (type(arrival_time))
    #     route=routestation(train_no=train_no,station_id=station_id,sequence_no=sequence_no,arrival_time=arrival_time,departure_time=departure_time)
    #     route.save()
        
    #     return HttpResponse ("Route added successfully")
    # else:
    #       HttpResponse("Error in adding Route") 
    # return render(request,"routestation.html")

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
        depart_date= request.POST.get("depart_date")
        clss=int(request.POST.get( "class"))
        
        
        
        # Query trains based on source station and destination station
        print(source,destination,type(depart_date))
        stn_src = station_master.objects.filter(station_code = source)
        print(stn_src)
        for station in stn_src:
            source_names = station.station_name
            
        print(source_names) 
        stn_des = station_master.objects.filter(station_code = destination)
        print(stn_des)
        for station in stn_des:
            des_names = station.station_name
        print(des_names)
        
        
        # query based on depart_date
        # try:
        #         parsed_date = datetime.strptime(depart_date, '%Y-%m-%d').date()
        # except ValueError:
        #         # Handle the case when date is not in the expected format
        #         return HttpResponse("Invalid date format. Please use YYYY-MM-DD.")
        # print(parsed_date)
        filtered_trains=[]
        rdes = train_schedule.objects.filter(
        
            station_code_id=destination,
        ).values()
        
        print(rdes)
        for  i in rdes:
             t_no=i["train_no_id"]
             print("the t_no  ",t_no)
             # distance of destination
             ddist = i['distance']
             print(ddist)
             day=i['day']
             arr=str(i['arrival_time'])
             print("this is for arival time",arr)
             sdes=train_schedule.objects.filter(train_no_id = t_no,station_code_id=source).values()
             print("sdes",sdes)
             for  j in sdes:
                 print(j['station_code_id'])
                 # distance at source
                 sdist=j['distance']
                 print(sdist,"is the dist from source")
                 depart_time=str(j['depart_time'])
                 print("depart time.",depart_time)
                 print(j['seq'],i['seq'])

                 if j['seq'] < i['seq'] :
                      
                    t_name = train_master.objects.filter(train_no=t_no).values()
                    for  k in t_name:
                         
                         filtered_trains.append(k)

        # find tottal diatance between source and detination
        total_dist=int(ddist)-int(sdist)
        print(total_dist,"is the total distance.",clss)
        if(clss==1):
             fare=total_dist*0.80
        elif(clss==2):
             fare=(total_dist*0.80)*2
        elif(clss==3):
             fare=(total_dist*0.80)*3
        else:
             fare=(total_dist*0.80)*4
              
        # parsed date of depart,time and arrival time
        dep_datetime=datetime.strptime(depart_date+' '+depart_time,'%Y-%m-%d %H:%M:%S')
        arr_time=datetime.strptime(arr, '%H:%M:%S').time()

        # calculate arivaldatetime
        if arr_time < dep_datetime.time() :
            arr_datetime=dep_datetime + timedelta(days=1)
        else:
            arr_datetime=dep_datetime
            
        arr_date = arr_datetime.strftime('%Y-%m-%d')
        print("filters trains",filtered_trains)
        station = {
            'src': source_names,
            'dest':des_names,
            
        }   
        try:   
            # Convert time objects to strings
            filtered_trains_serialized = []
            for train in filtered_trains:
                train_data = {
                    'train_no': train['train_no'],
                    'train_name': train['train_name'],
                    # Convert time objects to strings
                    'arrival_time': str(train['arrival_time']),
                    'departure_time': str(train['depart_time']),
                    'journey_duration': train['journey_duration'],
                    # Add other fields as needed
                }
            
            filtered_trains_serialized.append(train_data)
        
            # Store the serialized data in the session
            request.session["info"] = json.dumps({"trains": filtered_trains_serialized, "station": station}, cls=DjangoJSONEncoder)
            #print(t_no,sdes)
        except:
            print("Error in serializing data")
            messages.error(request, "No trains found")


        dat={
             'arrival_time':arr,
             'depart_time':str(depart_time),
             'depart_date':str(depart_date),
             'arrival_date':arr_date
        }
        request.session["dat"]= json.dumps(dat,cls=DjangoJSONEncoder) 
        request.session["fare"]=fare
       
       
       
        return HttpResponseRedirect('/displaytn')
        # return render(request,"searchedtrains.html",{ "trains": filtered_trains , "station": station})
       #You can do further processing with the 'trains' queryset

    else:
        # If it's a GET request, create an empty form
      print("else condn chal rhi hai")

    return render(request, 'srchtrn.html' )
def displaytn(request):          
     session_data_json=request.session.get('info')
     print ("Session Data Json ",type(session_data_json))
     fare=request.session.get('fare',None)
     datee=request.session.get( 'dat', None)
     dat=json.loads(datee) 
     if  not session_data_json :
          return HttpResponseRedirect('/dashboard')
     else:  
          session_data=json.loads(session_data_json)
          stations=session_data.get('station',{})
          trains=session_data.get('trains',[])
          print(stations)
         
     return  render(request,'searchedtrains.html',{"trains":trains,'station':stations,'fare':fare,'dat':dat}) 
    
     
def addpass(request):      
     return render(request, 'addpass.html')

#here we have all details of passengers and their respective trains. which will be  sent to payment gateway for booking ticket.
def reviewdetails(request):
    if  request.method=='POST':

        passenger_count = int(request.POST.get('passengerCount', 0))
        print(passenger_count)
        passengers = []
        for i in range(1, passenger_count + 1):
            
            name = request.POST.get(f'name{i}', '')
            age = int(request.POST.get(f'age{i}', 0))
            gender = request.POST.get(f'gender{i}','')
            passengers.append({'name': name, 'age': age, 'gender': gender })
            # passen=passenger_master(name=name,age=age,gender=gender)
            # passen.save()
        
        request.session['passengers'] = passengers
        print("passengers information in add passengers.",passengers)
    session_data_json= request.session.get('info')
    session_data=json.loads(session_data_json)
    station=session_data.get("station",{})
    print(station)
    trains=session_data.get("trains",[])
    print(trains)
    passengers=request.session.get('passengers',None)
    if passengers is None:
       return HttpResponseRedirect("/addpass?back=/reviewdetails/")
    else:
    #    context={"train":trains,"stn":station,"pax":passengers}
       
       print(passengers)
       return render(request,'revtktdet.html',{"trains":trains,"station":station,"paxs":passengers})

    #    return render(request,'bookingdetail.html',context)    

# @login_required
# def booknow(request):
#    try:
#       user=User.objects.get(username=request.user.username)
#       info=request.session.get('info')
#       if not info:
#           return HttpResponseRedirect('/searchTrain')
#       else:
#            stns=info["stations"]
#            trns=info["trains"]
#            paxs=request.session.get('passengers')
#            bkng=ticket_master(user=user,train=trns[0],from_station=stns[0].id,to_station=stns[1].id,no_of_passengers=len
    return render(request,'revtktdet.html')

def booking(request):
     session_data_json=request.session.get('info')
     session_data=json.loads(session_data_json)
     stations=session_data.get("stations",{})
     trains=session_data.get("trains",[])
     tr=[]
     for item in trains:
          try:
               train_no=item["train_no"]
               train_name=item["train_name"]
          except:
               pass
     
     tr.append({'train_no':train_no, 'train_name':train_name})
     station_from=stations['source']
     station_to=stations['destination']
# js_file_path='static/jsfiles/stations.json'
# json_data = open(js_file_path,'r')
# stations = json.loads(json_data.read())
# st_to_create  = []
# for d in stations["features"]:
#     data = d["properties"]
#     st_to_create.append(
#         station_master(
#             state=data["state"],
#             station_code=data["code"],
#             station_name=data["name"],
#             zone=data["zone"],
#             location=data["address"]
#         )
#     )
# station_master.objects.bulk_create(st_to_create)
# print('Data inserted successfully')

# to delete all stations from table
# try:
#     station_master.objects.all().delete()
#     print("dleted successfully.")
# except:
#     print("No Data to delete")


